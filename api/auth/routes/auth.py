from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from config.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import timedelta
from typing import List
from jose import jwt, JWTError
from api.auth.models import User
from api.auth.schemas import User as UserSchema, UserUpdate, Token
from config.utils import verify_password
from api.auth.routes.token import create_access_token, create_refresh_token, update_tokens, set_tokens_cookie, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from api.auth.routes.session import start_user_session, end_user_session

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
    if not user or not verify_password(password, user.hashed_password):
        return None
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
    try:
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

        response_data = {
            "access_token": access_token,
            "detail": "Успешная авторизация"
        }

        response = JSONResponse(status_code=status.HTTP_200_OK, content=response_data)
        set_tokens_cookie(response, refresh_token)
        return response
    except HTTPException as e:
        await db.rollback()
        raise e
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")

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

# Выход
@router.post("/logout")
async def logout(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    response = JSONResponse({"detail": "Вы успешно вышли из системы"})
    await end_user_session(current_user.id, db, response)
    return response
