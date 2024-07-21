from fastapi import APIRouter, Depends, HTTPException
from config.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from api.auth.models import User, Role, UserSession
from api.auth.schemas import UserCreate, UserUpdate,UserDelete, User as UserSchema
from api.auth.routes.roles import get_role
from api.auth.routes.auth import role_required
from config.utils import get_password_hash
from datetime import datetime
from typing import List, Dict

router = APIRouter()

# Инициализируем первичного пользователя
async def create_initial_user(db: AsyncSession):
    result = await db.execute(select(User))
    users_exist = result.scalars().first()
    if not users_exist:
        admin_role = await get_role(db, "admin")
        if not admin_role:
            print("Роль 'admin' не найдена. Создайте роль 'admin' и повторите попытку.")
            return
        initial_user = User(
            username="admin",
            first_name="",
            last_name="",
            email="admin@mail.com",
            phone="",
            address="",
            company="",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            hashed_password=get_password_hash("admin"),
            role_id=admin_role.id,
            is_active=True,  
            is_verified=True  
        )
        db.add(initial_user)
        await db.commit()
        print("Пользователь-администратор создан") 
    else:
        print("Таблица с пользователями существует. Запуск приложения...")

# Загружаем связные данные
async def load_user_relations(user: User, db: AsyncSession):
    user_role = await db.execute(select(Role).filter(Role.id == user.role_id))
    user.role = user_role.scalars().first()
    
    user_sessions = await db.execute(select(User).options(selectinload(User.sessions)).filter(User.id == user.id))
    user.sessions = user_sessions.scalars().first().sessions

# Создание пользователя
@router.post("/", response_model=List[UserSchema])
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db), current_user: User = role_required(["admin"])):
    try:
        # Проверяем, существует ли пользователь с таким username или email
        result = await db.execute(select(User).filter((User.username == user.username) | (User.email == user.email)))
        current_user = result.scalars().first()
        
        if current_user:
            raise HTTPException(status_code=400, detail="Пользователь существует")

        # Создаем нового пользователя
        new_user_data = user.dict(exclude={"password"})  # Исключаем пароль
        new_user_data["hashed_password"] = get_password_hash(user.password)  # Хэшируем пароль
        new_user_data["created_at"] = datetime.utcnow()

        if not new_user_data.get("role_id"):
            default_role = await get_role(db)
            new_user_data["role_id"] = default_role.id

        new_user = User(**new_user_data)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        await load_user_relations(new_user, db)

        # Возвращаем обновленные данные после создания
        updated_users = await db.execute(select(User).options(selectinload(User.role), selectinload(User.sessions)))
        users = updated_users.scalars().all()
        return [UserSchema.from_orm(user) for user in users]
    except IntegrityError as e:
        await db.rollback()
        if 'foreign key constraint' in str(e.orig):
            raise HTTPException(status_code=400, detail="Невозможно создать пользователя. Укажите роль.")
        else:
            raise HTTPException(status_code=400, detail="Ошибка целостности данных: " + str(e.orig))
    except HTTPException as e:
        raise e
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при создании пользователя: " + str(e))

# Список пользователей
@router.get("/", response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db), current_user: User = role_required(["admin"])):
    try:
        result = await db.execute(
            select(User)
            .options(selectinload(User.role))
            .options(selectinload(User.sessions))
        )
        users = result.scalars().all()

        return [UserSchema.from_orm(user) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Данные пользователя
@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db),  current_user: User = role_required(["admin"])):
    try:
        result = await db.execute(
            select(User)
            .options(selectinload(User.role))
            .options(selectinload(User.sessions))
            .filter(User.id == user_id)
        )
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        return UserSchema.from_orm(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Обновить данные пользователя
@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db),  current_user: User = role_required(["admin"])):
    try:
        # Fetch the user
        result = await db.execute(select(User).options(selectinload(User.role), selectinload(User.sessions)).filter(User.id == user_id))
        db_user = result.scalars().first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        if user.username:
            existing_user = await db.execute(select(User).filter(User.username == user.username, User.id != user_id))
            if existing_user.scalars().first():
                raise HTTPException(status_code=400, detail="Указанное имя пользователя уже существует")

        if user.email:
            existing_user = await db.execute(select(User).filter(User.email == user.email, User.id != user_id))
            if existing_user.scalars().first():
                raise HTTPException(status_code=400, detail="Указанный адрес электронной почты уже существует")

        # Prepare update data
        update_data = user.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)

        await load_user_relations(db_user, db)

        # Return the updated user
        return UserSchema.from_orm(db_user)

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Пользователь с таким именем или email уже существует")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
# Удалить пользователя
@router.delete("/{user_id}", response_model=UserDelete)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db),  current_user: User = role_required(["admin"])):
    # Проверка, является ли пользователь первичным
    if user_id == 1:
        raise HTTPException(status_code=403, detail="Нельзя удалить первичного пользователя")
    
    # Получение пользователя для проверки существования
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail=f"Пользователь с ID {user_id} не найден")
    
    # Сохранение данных пользователя перед удалением
    user_data = UserSchema.from_orm(user)
    
    # Завершение сессий
    await db.execute(delete(UserSession).where(UserSession.user_id == user_id))
    
    # Удаление пользователя
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()
    
    return UserDelete(detail=f"Пользователь ID {user_id} - {user.username} успешно удален", user=user_data)
