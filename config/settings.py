import sys
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware

# Добавьте корневую директорию проекта в путь поиска модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Папка с шаблонами
templates = Jinja2Templates(directory="templates")

# Импорт Middleware
from config.middleware import db_session_middleware, add_cors_middleware
from api.auth.routes.users import create_initial_user
from config.db import async_session
from config.router import get_routers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Expeditor",
        swagger_ui_parameters={
            "docExpansion": "none",  # сворачиваем вкладки по умолчанию
            "displayRequestDuration": True,
            "filter": True,
        }
    )

    # Подключение CORS middleware
    add_cors_middleware(app)

    # Подключение DB session middleware
    app.add_middleware(BaseHTTPMiddleware, dispatch=db_session_middleware)

    # Подключение Traffic middleware (раскомментируйте, если у вас есть TrafficMiddleware)
    # app.add_middleware(TrafficMiddleware)

    # Подключение статических файлов
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Обработчик для ошибки 404
    @app.exception_handler(404)
    async def not_found_exception_handler(request: Request, exc: HTTPException):
        return templates.TemplateResponse(
            "layouts/errors.html",
            {"request": request, "status_code": 404, "message": "Страница не найдена"},
            status_code=404,
        )

    # Вызов асинхронной функции для создания первичного пользователя
    @app.on_event("startup")
    async def startup_event():
        async with async_session() as session:
            await create_initial_user(session)

    # Подключение роутеров
    get_routers(app)

    return app


app = create_app()
