import logging

def setup_logging():
    # Установим уровень логирования для SQLAlchemy на WARNING
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    # Настройка базовой конфигурации логгера
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Вывод логов в консоль
        ]
    )

# Вызовем функцию настройки логирования
setup_logging()