
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import datetime
from api.auth.models import Role, User, UserSession
from typing import List, Dict
from jose import jwt, JWTError  
from api.auth.routes.token import SECRET_KEY, ALGORITHM
from config.db import get_db
from config.utils import get_password_hash, verify_password

bearer_scheme = HTTPBearer()

# Получаем роль
async def get_role(db: AsyncSession, role_name: str = "user") -> Role:
    result = await db.execute(select(Role).filter_by(name=role_name))
    role = result.scalars().first()

    # Если роли не определены, создаем "admin", "user" и "guest" при первой записи
    if not role:
        first_role = await db.execute(select(Role))
        if first_role.scalars().first() is None:
            roles_to_create = [
                {"name": "admin", "description": "Администратор"},
                {"name": "user", "description": "Пользователь"},
                {"name": "guest", "description": "Гость"}
            ]
            for role_data in roles_to_create:
                new_role = Role(**role_data)
                db.add(new_role)
            await db.commit()
            # Возвращаем роль "admin" для первого пользователя
            role = await db.execute(select(Role).filter_by(name="admin"))
            role = role.scalars().first()
        else:
            role = Role(name=role_name, description="Пользователь")
            db.add(role)
            await db.commit()
            await db.refresh(role)

    return role


# Проверки ролей
def role_required(roles: List[str]):
    async def check_roles(current_user: User = Depends(user_status), db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User).filter(User.id == current_user.id).options(selectinload(User.role)))
        user = result.scalars().first()
        if not user or user.role.name not in roles:
            raise HTTPException(status_code=403, detail="Недостаточно прав")
        return current_user
    
    return Depends(check_roles)
  
  
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


# Текущий пользователь
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не авторизован",
        headers={"WWW-Authenticate": "Bearer"},
    )
    forbidden_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Доступ запрещен",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
    
    if token is None:
        raise forbidden_exception
    
    return user


# Статус текущего пользователя
async def user_status(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Неактивный пользователь")
    return current_user


# Верификация пользователя
async def verify_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Имя пользователя не существует")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Учетная запись не активна")
    return user


# Получение текущей сессии по user_id
async def get_current_session(user_id: int, db: AsyncSession):
    result = await db.execute(select(UserSession).filter(UserSession.user_id == user_id, UserSession.session_end == None))
    session = result.scalars().first()
    return session


# Cтарт сессии
async def start_user_session(user_id: int, refresh_token: str, ip_address: str, user_agent: str, traffic: int, db: AsyncSession):
    result = await db.execute(select(UserSession).filter(UserSession.user_id == user_id))
    session = result.scalars().first()

    if session:
        session.traffic += traffic
        session.refresh_token = refresh_token
        session.session_start = datetime.utcnow()
        session.session_end = None
    else:
        new_session = UserSession(
            refresh_token=refresh_token,
            session_start=datetime.utcnow(),
            user_id=user_id,
            traffic=traffic,
            ip_address=ip_address,
            device_info=user_agent
        )
        db.add(new_session)
    await db.commit()


# Окончание сессии
async def end_user_session(user_id: int, db: AsyncSession, response: Response):
    session = await get_current_session(user_id, db)

    if session:
        session.session_end = datetime.utcnow()
        session.refresh_token = None
        await db.commit()
 

