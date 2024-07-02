import sys
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Загрузить переменные окружения из .env файла
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Добавьте корневую директорию проекта в путь поиска модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Папка с шаблонами
templates = Jinja2Templates(directory="templates")

<<<<<<< HEAD
from config.middleware import add_cors_middleware
from config.middleware import TrafficMiddleware
=======
from config.middleware import add_cors_middleware, db_session_middleware
>>>>>>> f474fef (Updated)
from api.auth.routes.users import create_initial_user
from config.db import async_session

def create_app() -> FastAPI:
<<<<<<< HEAD
    app = FastAPI(title="Expeditor")

    # Добавление CORS middleware
    add_cors_middleware(app)
    
    # Добавление Traffic middleware
    app.add_middleware(TrafficMiddleware)
    
=======
    app = FastAPI(
        title="Expeditor",
        swagger_ui_parameters={
            "docExpansion": "none"  # сворачиваем вкладки по умолчанию
        }
    )

    # Добавление CORS middleware
    add_cors_middleware(app)

    # Добавляем DB session middleware
    app.middleware("http")(db_session_middleware)

>>>>>>> f474fef (Updated)
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

    return app

app = create_app()
