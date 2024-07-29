from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm,HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta
from jose import jwt, JWTError  
from config.db import get_db
from config.utils import verify_password, get_password_hash
from api.auth.models import User
from api.auth.schemas import User as UserSchema, UserUpdate, Token
from api.auth.controllers import get_current_user,verify_user, start_user_session, end_user_session, get_current_session
from api.auth.routes.token import create_access_token, create_refresh_token, update_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta



router = APIRouter()

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

    if user_update.password:
        if not user_update.old_password or not verify_password(user_update.old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Неправильный текущий пароль")
        user.hashed_password = get_password_hash(user_update.password)

    update_data = user_update.dict(exclude_unset=True, exclude={"old_password", "password"})
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
@router.post("/token", response_model=Token)
async def refresh_token(request: Request, response: Response, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        # Получаем текущую сессию пользователя из базы данных
        user_session = await get_current_session(current_user.id, db)
        
        if not user_session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходима авторизация")

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
