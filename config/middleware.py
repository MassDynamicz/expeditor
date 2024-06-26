# config/middleware.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.auth.models import UserSession
from config.db import get_db
import asyncio
origins = [
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:5173",
]

def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Middleware для подсчета трафика
class TrafficMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        response = await call_next(request)

        if token:
            token = token.replace("Bearer ", "")
            await asyncio.get_event_loop().run_in_executor(None, self.update_traffic, token, len(request.body), len(response.body))

        return response

    def update_traffic(self, token: str, request_size: int, response_size: int):
        async def update():
            async with get_db() as db:
                session = await self.get_user_session(db, token)
                if session:
                    session.traffic += request_size + response_size
                    await db.commit()
        asyncio.run(update())

    async def get_user_session(self, db: AsyncSession, token: str) -> UserSession:
        result = await db.execute(select(UserSession).filter(UserSession.token == token))
        return result.scalars().first()
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        response = await call_next(request)

        if token:
            token = token.replace("Bearer ", "")
            async with get_db() as db:
                session = await self.get_user_session(db, token)
                if session:
                    session.traffic += len(request.body) + len(response.body)
                    await db.commit()

        return response

    async def get_user_session(self, db: AsyncSession, token: str) -> UserSession:
        result = await db.execute(select(UserSession).filter(UserSession.token == token))
        return result.scalars().first()