
from config.db import async_session, get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging
from jose import jwt, JWTError
from api.auth.models import User, UserSession
from api.auth.routes.token import update_tokens, set_tokens_cookie, SECRET_KEY, ALGORITHM
from api.auth.routes.session import end_user_session

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

        # Check and update tokens if necessary
        auth_header = request.headers.get('Authorization')
        refresh_token = request.cookies.get("refresh_token")

        if auth_header:
            token_type, token = auth_header.split()
            if token_type.lower() == 'bearer':
                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                except JWTError:
                    if refresh_token:
                        try:
                            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
                            new_access_token, new_refresh_token = update_tokens(refresh_token)
                            logger.info(f"Access token обновлен для пользователя {payload.get('username')}")
                            response = await call_next(request)
                            response.headers["Authorization"] = f"Bearer {new_access_token}"
                            set_tokens_cookie(response, new_refresh_token)
                            return response
                        except JWTError:
                            # Refresh token is invalid or expired
                            await end_user_session(payload.get("user_id"), session)
                            logger.info(f"Refresh token истек для пользователя {payload.get('username')}")
                            response = JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Refresh token истек"})
                            response.delete_cookie("refresh_token")
                            return response

        elif refresh_token:
            try:
                payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            except JWTError:
                # Refresh token is invalid or expired
                await end_user_session(payload.get("user_id"), session)
                logger.info(f"Refresh token истек для пользователя {payload.get('username')}")
                response = JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Refresh token истек"})
                response.delete_cookie("refresh_token")
                return response

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
