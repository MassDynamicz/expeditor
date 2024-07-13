# config/db.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
from dotenv import load_dotenv
load_dotenv(dotenv_path='config/.env')

# Параметры подключения из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Переключение на SQLITE
# DATABASE_URL = os.getenv("DATABASE_URL_SQLITE")

# Асинхронное подключение к бд
engine = create_async_engine(DATABASE_URL, echo=True)
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
