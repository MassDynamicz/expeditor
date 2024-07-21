from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import timedelta
from typing import List
from jose import jwt, JWTError  
from config.db import get_db
from config.utils import verify_password
from api.auth.models import User
from api.auth.schemas import User as UserSchema, UserUpdate, Token
from api.auth.routes.token import create_access_token, create_refresh_token, update_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from api.auth.routes.session import start_user_session, end_user_session, get_current_session
from api.auth.schemas import UserSession as UserSessionSchema
from datetime import timedelta
bearer_scheme = HTTPBearer()
router = APIRouter()

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

# Универсальная функция для проверки ролей
def role_required(roles: List[str]):
    async def check_roles(current_user: User = Depends(user_status), db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User).filter(User.id == current_user.id).options(selectinload(User.role)))
        user = result.scalars().first()
        if not user or user.role.name not in roles:
            raise HTTPException(status_code=403, detail="Недостаточно прав")
        return current_user
    
    return Depends(check_roles)

# Авторизация
@router.post("/login", response_model=Token)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await verify_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Имя пользователя или пароль указаны не верно")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": user.username, "user_id": user.id, "role": user.role_id}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"username": user.username, "user_id": user.id, "role": user.role_id})

    client_host = request.client.host
    user_agent = request.headers.get("User-Agent")
    content_length = request.headers.get("Content-Length")
    if content_length is not None:
        traffic = int(content_length)
    else:
        body = await request.body()
        traffic = len(body)

    await start_user_session(user.id, refresh_token, client_host, user_agent, traffic, db)

    response = JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Успешная авторизация", "access_token": access_token})
    return response

# Профиль пользователя
@router.get("/profile", response_model=UserSchema)
async def user_profile(current_user: User = Depends(get_current_user)):
    return current_user

# Обновление профиля
@router.patch("/profile", response_model=UserSchema)
async def update_user_profile(user_update: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(User).filter(User.id == current_user.id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if user_update.username:
        existing_user = await db.execute(select(User).filter(User.username == user_update.username, User.id != current_user.id))
        if existing_user.scalars().first():
            raise HTTPException(status_code=400, detail="Указанное имя пользователя уже существует")

    if user_update.email:
        existing_user = await db.execute(select(User).filter(User.email == user_update.email, User.id != current_user.id))
        if existing_user.scalars().first():
            raise HTTPException(status_code=400, detail="Указанный адрес электронной почты уже существует")

    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return user

# Текущая сессия
@router.get("/session")
async def get_session(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    session = await get_current_session(current_user.id, db)
    if session:
        return {
            "id": session.id,
            "user_id": session.user_id,
            "session_start": session.session_start,
            "session_end": session.session_end,
            "traffic": session.traffic,
            "ip_address": session.ip_address,
            "device_info": session.device_info,
        }
    return {"error": "Сессия не найдена"}

# Обновление токена
@router.post("/refresh", response_model=Token)
async def refresh_token(request: Request, response: Response, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        # Получаем текущую сессию пользователя из базы данных
        user_session = await get_current_session(current_user.id, db)
        
        if not user_session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходима повторная авторизация")

        refresh_token = user_session.refresh_token

        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")

        return await update_access_token(current_user.id, response)

    except JWTError:
        await end_user_session(current_user.id, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")


# Выход
@router.post("/logout")
async def logout(request: Request, response: Response, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    await end_user_session(current_user.id, db, response)
    return JSONResponse({"detail": "Вы успешно вышли из системы"})
