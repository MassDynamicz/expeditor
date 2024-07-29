import sys, os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from config.db import async_session
from config.middleware import add_cors_middleware, db_session_middleware
from config.router import get_routers
from api.auth.controllers import create_initial_user

# Добавьте корневую директорию проекта в путь поиска модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Папка с шаблонами
templates = Jinja2Templates(directory="templates")

def create_app() -> FastAPI:
    app = FastAPI(
        docs_url="/docs",
        redoc_url=None,
        title="Expeditor",
        description="Проект представляет собой асинхронное веб-приложение, созданное с использованием фреймворка FastAPI и SQLAlchemy для работы с базой данных.",
        swagger_ui_parameters={"docExpansion": "none","displayRequestDuration": True,"filter": True},
    )

    # Подключение CORS middleware
    add_cors_middleware(app)

    # Подключение DB session middleware
    app.add_middleware(BaseHTTPMiddleware, dispatch=db_session_middleware)

    # Подключение статических файлов
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Обработчик для ошибки 404
    @app.exception_handler(404)
    async def not_found_exception_handler(request: Request, exc: HTTPException):
        return templates.TemplateResponse(
            "layouts/errors.html",
            {"request": request, "status_code": 404,
                "message": "Страница не найдена"},
            status_code=404,
        )
        
    # Обработчик для ошибки 403
    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        if exc.status_code == status.HTTP_403_FORBIDDEN:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Доступ запрещен.\nНеобходима авторизация."},
            )
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
        
    # Запуск приложения
    @app.on_event("startup")
    async def startup_event():
        async with async_session() as session:
            # создание первичного пользователя
            await create_initial_user(session)

    # Подключение роутеров
    get_routers(app)

    return app

app = create_app()
