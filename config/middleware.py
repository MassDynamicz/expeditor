from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.auth.models import UserSession
from config.db import async_session
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

# CORS origins
origins = [
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:5173",
]

def add_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# DB session and traffic tracking middleware
async def db_session_middleware(request: Request, call_next):
    async with async_session() as session:
        request.state.db = session
        response = await call_next(request)

        # Traffic tracking
        token = request.headers.get("authorization")
        if token:
            token = token.split(" ")[1]

            result = await session.execute(select(UserSession).filter(UserSession.refresh_token == token, UserSession.session_end == None))
            user_session = result.scalars().first()

            if user_session:
                content_length = request.headers.get("Content-Length")
                if content_length:
                    traffic = int(content_length)
                else:
                    body = await request.body()
                    traffic = len(body)

                user_session.traffic += traffic
                await session.commit()

    return response
