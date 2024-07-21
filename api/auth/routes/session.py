#api.auth.routes.session.py
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from api.auth.models import UserSession

router = APIRouter()

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
 

