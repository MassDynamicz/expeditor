from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete
from datetime import datetime, timedelta
from config.db import get_db
from api.auth.models import User, UserSession
from api.auth.schemas import Login, Token
from config.utils import verify_password, create_access_token
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/login/", response_model=Token)
async def login(data: Login, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(
            select(User).options(selectinload(User.role)).filter(User.username == data.username)
        )
        user = result.scalars().first()
        if user is None or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")

        # Удаление старых сессий
        await db.execute(delete(UserSession).where(UserSession.user_id == user.id))

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "username": user.username,
                "role": user.role.name if user.role else None
            },
            expires_delta=access_token_expires
        )

        # Создание новой сессии для пользователя
        user_session = UserSession(
            user_id=user.id,
            token=access_token,
            session_start=datetime.utcnow(),
            traffic=0  # Начальное значение для трафика
        )
        db.add(user_session)

    await db.commit()
    await db.refresh(user_session)
    await db.refresh(user, ["role"])

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "role": user.role.name if user.role else None,
        "message": "Пользователь успешно авторизован" 
    }
