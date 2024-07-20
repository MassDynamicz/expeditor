# config/db.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Загрузка переменных окружения из файла .env
from dotenv import load_dotenv
load_dotenv(dotenv_path='config/.env')

# Использование DB_URL из переменных окружения
DB_URL = os.getenv("DB_URL")

# Если строка подключения содержит PostgreSQL, добавляем sslmode=require
if DB_URL and DB_URL.startswith("postgresql+asyncpg://"):
    DB_URL = DB_URL.replace("postgresql+asyncpg://", "postgresql+asyncpg://", 1) + "?ssl=true"

# Асинхронное подключение к бд
engine = create_async_engine(DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
