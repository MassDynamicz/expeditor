from config.db import async_session
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from sqlalchemy.future import select
from api.auth.models import UserSession
from sqlalchemy.ext.asyncio import AsyncSession
# CORS origins
origins = [
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:5173",
    "http://192.168.88.146:5173",
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

        try:
            response = await call_next(request)
            await track_traffic(request, session)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    return response

async def track_traffic(request: Request, session: AsyncSession):
    token = get_token_from_request(request)
    if token:
        user_session = await get_user_session_by_token(session, token)
        if user_session:
            traffic = await calculate_traffic(request)
            user_session.traffic += traffic
            await session.commit()

def get_token_from_request(request: Request):
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return None

async def get_user_session_by_token(session: AsyncSession, token: str):
    result = await session.execute(select(UserSession).filter(UserSession.refresh_token == token, UserSession.session_end == None))
    return result.scalars().first()

async def calculate_traffic(request: Request):
    content_length = request.headers.get("Content-Length")
    if content_length:
        return int(content_length)
    body = await request.body()
    return len(body)
