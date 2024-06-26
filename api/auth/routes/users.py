# auth/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from config.db import get_db
from api.auth.models import User, Role, Permission
from api.auth.schemas import UserCreate,UserUpdate, User as UserSchema
from config.utils import get_password_hash
from datetime import datetime
from typing import List

router = APIRouter()

#получаем или добавляем роли
async def get_or_create_role(db: AsyncSession, role_name: str, permissions: List[Permission] = None) -> Role:
    result = await db.execute(select(Role).filter_by(name=role_name))
    role = result.scalars().first()
    if not role:
        role = Role(name=role_name, description=f"{role_name.capitalize()} role")
        if permissions:
            role.permissions.extend(permissions)
        db.add(role)
        await db.commit()
    return role

#получаем или добавляем права доступа
async def get_or_create_permission(db: AsyncSession, name: str, description: str) -> Permission:
    result = await db.execute(select(Permission).filter_by(name=name))
    permission = result.scalars().first()
    if not permission:
        permission = Permission(name=name, description=description)
        db.add(permission)
        await db.commit()
    return permission

#инициализируем первичного пользователя
async def create_initial_user(db: AsyncSession):
    result = await db.execute(select(User))
    users_exist = result.scalars().first()
    if not users_exist:
        permissions = [
            await get_or_create_permission(db, "create", "Создание"),
            await get_or_create_permission(db, "read", "Просмотр"),
            await get_or_create_permission(db, "update", "Редактирование"),
            await get_or_create_permission(db, "delete", "Удаление")
        ]
        admin_role = await get_or_create_role(db, "admin", permissions)
        initial_user = User(
            username="admin",
            first_name="",
            last_name="",
            email="admin@mail.com",
            phone="",
            address="",
            company="",
            status=True,
            created_at=datetime.utcnow(),
            hashed_password=get_password_hash("admin"),
            role=admin_role
        )
        db.add(initial_user)
        try:
            await db.commit()
            print("Пользователь-администратор создан")
        except IntegrityError:
            await db.rollback()
            print("Первичный админ существует")
    else:
        print("Таблица с пользователями существует. Запуск приложения...")

#определяем роль по умолчанию
async def get_default_role(db: AsyncSession) -> Role:
    return await get_or_create_role(db, "user", [await get_or_create_permission(db, "read_own", "Просмотр собственных данных")])

#загружаем связные данные
async def load_user_relations(user: User, db: AsyncSession):
    user_role = await db.execute(select(Role).options(selectinload(Role.permissions)).filter(Role.id == user.role_id))
    user.role = user_role.scalars().first()
    user_sessions = await db.execute(select(User).options(selectinload(User.sessions)).filter(User.id == user.id))
    user.sessions = user_sessions.scalars().first().sessions

# Создание пользователя
@router.post("/", response_model=UserSchema)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).filter((User.username == user.username) | (User.email == user.email)))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь существует")

        new_user_data = user.dict(exclude={"password"})  # Исключаем пароль
        new_user_data["hashed_password"] = get_password_hash(user.password)  # Хэшируем пароль
        new_user_data["created_at"] = datetime.utcnow()

        if not new_user_data.get("role_id"):
            default_role = await get_default_role(db)
            new_user_data["role_id"] = default_role.id
            print(f"Присвоена роль 'user' с id: {default_role.id} для нового пользователя")

        new_user = User(**new_user_data)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        await load_user_relations(new_user, db)
        print(f"Создан новый пользователь: {new_user.username}")

        return new_user
    except IntegrityError as e:
        await db.rollback()
        print(f"Ошибка создания пользователя из-за ошибки целостности: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
    except Exception as e:
        print(f"Неожиданная ошибка при создании пользователя: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
# Список пользователей
@router.get("/", response_model=List[UserSchema])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(User)
            .options(selectinload(User.role).selectinload(Role.permissions))
            .options(selectinload(User.sessions))
            .offset(skip).limit(limit)
        )
        users = result.scalars().all()
        return [UserSchema.from_orm(user) for user in users]
    except Exception as e:
        print(f"Ошибка чтения пользователей: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read users: {str(e)}")

# Данные пользователя
@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(User)
            .options(selectinload(User.role).selectinload(Role.permissions))
            .options(selectinload(User.sessions))
            .filter(User.id == user_id)
        )
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        return UserSchema.from_orm(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Обновить пользователя
@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).options(selectinload(User.role), selectinload(User.sessions)).filter(User.id == user_id))
        db_user = result.scalars().first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        update_data = user.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)

        await load_user_relations(db_user, db)
        
        return db_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Удалить пользователя
@router.delete("/{user_id}", response_model=UserSchema)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).options(selectinload(User.role), selectinload(User.sessions)).filter(User.id == user_id))
        user = result.scalars().first()

        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Открепляем связанные данные
        user.role = None
        user.sessions = []

        await db.delete(user)
        await db.commit()

        return user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
