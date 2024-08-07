#api.auth.routes.session.py
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from api.auth.models import UserSession
from api.auth.routes.token import clear_cookies

# Cтарт сессии
async def start_user_session(user_id: int, refresh_token: str, ip_address: str, user_agent: str, traffic: int, db: AsyncSession):
    result = await db.execute(select(UserSession).filter(UserSession.user_id == user_id))
    session = result.scalars().first()

    if session:
        session.traffic += traffic
        session.refresh_token = refresh_token
        session.session_start = datetime.utcnow()
        session.session_end = None  # Обнуляем дату окончания, чтобы сессия считалась активной
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
    result = await db.execute(select(UserSession).filter(UserSession.user_id == user_id, UserSession.session_end == None))
    session = result.scalars().first()

    if session:
        session.session_end = datetime.utcnow()
        clear_cookies(response)
        await db.commit()
