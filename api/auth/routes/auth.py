from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta
from config.db import get_db
from jose import jwt, JWTError
from api.auth.models import User
from api.auth.schemas import User as UserSchema, Token
from config.utils import verify_password
from api.auth.routes.token import create_access_token, create_refresh_token, update_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from api.auth.routes.session import start_user_session, end_user_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()


# Проверка пользователя и пароля
async def verify_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Авторизация
@router.post("/login", response_model=Token)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        user = await verify_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Имя пользователя или пароль указаны не верно")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username, "user_id": user.id, "role": user.role_id}, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(data={"sub": user.username, "user_id": user.id, "role": user.role_id})

        # Получение информации
        client_host = request.client.host
        user_agent = request.headers.get("User-Agent")
        content_length = request.headers.get("Content-Length")
        if content_length is not None:
            traffic = int(content_length)
        else:
            body = await request.body()
            traffic = len(body)

        # Пользовательская сессия
        await start_user_session(user.id, refresh_token, client_host, user_agent, traffic, db)

        # Установка статуса и уведомления
        response_data = {
            "access_token": access_token,
            "token_type": "bearer",
            "detail": "Успешная авторизация"
        }

        return JSONResponse(status_code=status.HTTP_200_OK, content=response_data)
    except HTTPException as e:
        await db.rollback()
        raise e
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")

# Получение текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
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

# Получаем профиль пользователя
@router.get("/profile", response_model=UserSchema)
async def user_profile(current_user: User = Depends(get_current_user)):
    return current_user

# Выйти
@router.post("/logout")
async def logout(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    token = request.headers.get("authorization").split(" ")[1]
    await end_user_session(current_user.id, db)
    return {"msg": "Вы успешно вышли из системы"}
