import os
import importlib


def import_all_models():
    # Получаем путь текущей директории
    base_path = os.path.dirname(__file__)

    # Проходим по всем вложенным директориям
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == 'models.py':
                # Получаем относительный путь к файлу models.py
                relative_path = os.path.relpath(os.path.join(root, file), base_path)
                # Преобразуем путь в формат импорта модуля (заменяем / на . и удаляем .py)
                module_name = relative_path.replace(os.sep, '.')[:-3]
                # Импортируем модуль
                importlib.import_module(f'.{module_name}', package='api')

# Вызываем функцию для импорта всех моделей


import_all_models()
