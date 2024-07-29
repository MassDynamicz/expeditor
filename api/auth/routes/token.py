import os
from config.db import async_session
from fastapi import HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from jose import jwt, JWTError  
from api.auth.schemas import Token 
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))

# Создать токен доступа
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Создать токен обновления
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Проверка токена доступа
async def check_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Обновление токена доступа
async def update_access_token(user_id: int, response: Response) -> Token:
    try:
        async with async_session() as session:
            from api.auth.controllers import get_current_session  # Локальный импорт
            user_session = await get_current_session(user_id, session)

            if not user_session:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходима повторная авторизация")

            refresh_token = user_session.refresh_token

            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("username")
            role_id = payload.get("role")

            # Создать новый access токен
            new_access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            new_access_token = create_access_token(data={"username": username, "user_id": user_id, "role": role_id}, expires_delta=new_access_token_expires)

            # Отправить новый access токен в заголовке ответа
            response.headers['Authorization'] = f'Bearer {new_access_token}'

            return Token(access_token=new_access_token, token_type="bearer")
    except JWTError:
        async with async_session() as session:
            from api.auth.routes.session import end_user_session  # Локальный импорт
            await end_user_session(user_id, session)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходимо авторизоваться")
