import os
from datetime import datetime, timedelta
from jose import jwt, JWTError  
from fastapi import HTTPException, status
from fastapi.responses import Response
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def update_tokens(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: int = payload.get("user_id")
        role_id: int = payload.get("role")
        if username is None or user_id is None:
            raise JWTError("Invalid refresh token")

        new_access_token = create_access_token(data={"username": username, "user_id": user_id, "role": role_id})
        new_refresh_token = create_refresh_token(data={"username": username, "user_id": user_id, "role": role_id})

        return new_access_token, new_refresh_token
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

def set_tokens_cookie(response: Response, refresh_token: str):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60  # в секундах
    )
    
# Удаление куки
def clear_cookies(response: Response):
    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")