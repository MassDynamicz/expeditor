from __future__ import with_statement
import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path
import pkgutil
import importlib

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection

from alembic import context

# Добавляем корневой каталог проекта в sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

config = context.config

fileConfig(config.config_file_name)


# Автоматический импорт всех моделей из пакета api
def import_submodules(package_name):
    """Импортирует все подмодули в заданном пакете."""
    package = importlib.import_module(package_name)
    for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        importlib.import_module(module_name)


import_submodules('api')


# Загрузка переменных окружения из файла .env
load_dotenv(dotenv_path='config/.env')
# Установка URL подключения из переменной окружения
database_url = os.getenv("DB_URL")

if not database_url:
    raise ValueError("DATABASE_URL не задана в файле .env")

config.set_main_option('sqlalchemy.url', database_url)


# Импортируем базовый класс и собираем метаданные моделей
from api.auth.models import Base  # Импортируем Base из ваших моделей

target_metadata = Base.metadata


def do_run_migrations(connection: AsyncConnection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table='migrations',
        render_as_batch=True  # Добавляем эту строку для включения режима пакетных операций
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        version_table='migrations',
        render_as_batch=True  # Добавляем эту строку для включения режима пакетных операций
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    asyncio.run(run_migrations_online())
