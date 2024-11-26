import os, importlib
from fastapi import FastAPI, APIRouter
from config.utils import camel_to_kebab
from typing import List, Dict

# Словарь для сопоставления имен файлов с тегами
tag_mappings = {
    "auth": "Авторизация",
    "roles": "Роли и права доступа",
    "users": "Пользователи",
    "session": "Сессии",
    "currency": "Валюты",
    "country": "Страны",
    "vat": "НДС",
    "bank": "Банки",
    "organization": "Организации",
    "contractor": "Контрагенты",
    "contract": "Договора",
    "bank-account": "Банковские счета",
    "wagon-type": "Роды подвижного состава",
    "service-type": "Виды услуг",
    "wagon": "Вагоны",
    "container": "Контейнеры",
    "etsng": "Грузы по ЕТСНГ",
    "gng": "Грузы по ГНГ",
    "operation": "Операции по Ж/Д",
    "territory": "Территории Ж/Д",
    "station": "Станции Ж/Д",
    "dislocation": "Дислокация",
    "rail-way-code": "Коды Ж/Д",
    "subcode": "Подкоды",
    "order-rail-way": "Заявки Ж/Д",
    "order-rail-way-route": "Заявки Ж/Д - маршруты",
}

# Словарь исключений для префиксов
prefix_exceptions = ["auth"]

routers_sorted = []  # Глобальный список маршрутов

def get_routers(app: FastAPI):
    global routers_sorted
    base_dir = "api"
    routers = []

    for root, dirs, files in os.walk(base_dir):
        if "routes.py" in files:
            module_path = os.path.join(root, "routes.py")
            module_import_path = module_path.replace("/", ".").replace("\\", ".").replace(".py", "")
            module = importlib.import_module(module_import_path)
            router = getattr(module, "router", None)

            if router and isinstance(router, APIRouter):
                folder_name = os.path.basename(root)
                folder_name_kebab = camel_to_kebab(folder_name)
                if folder_name_kebab in prefix_exceptions:
                    prefix = ""
                else:
                    prefix = f"/{folder_name_kebab}"
                tag = tag_mappings.get(folder_name_kebab, folder_name.replace("_", " ").title())
                routers.append((prefix, tag, router))

        if "routes" in dirs:
            routes_dir = os.path.join(root, "routes")
            for file in os.listdir(routes_dir):
                if file.endswith(".py"):
                    module_path = os.path.join(routes_dir, file)
                    module_import_path = module_path.replace("/", ".").replace("\\", ".").replace(".py", "")
                    module = importlib.import_module(module_import_path)
                    router = getattr(module, "router", None)

                    if router and isinstance(router, APIRouter):
                        file_name = file.replace(".py", "")
                        file_name_kebab = camel_to_kebab(file_name)
                        if file_name_kebab in prefix_exceptions:
                            prefix = ""
                        else:
                            prefix = f"/{file_name_kebab}"
                        tag = tag_mappings.get(file_name_kebab, file_name.replace("_", " ").title())
                        routers.append((prefix, tag, router))

    routers_sorted = sorted(routers, key=lambda x: x[1])
    for prefix, tag, router in routers_sorted:
        app.include_router(router, prefix=prefix, tags=[tag])

# Пример API для получения списка рубрик
app = FastAPI()

@app.get("/rubrics/", response_model=List[Dict[str, str]])
async def get_rubrics():
    # Возвращаем список всех маршрутов и их тегов
    return [{"prefix": prefix, "tag": tag} for prefix, tag, _ in routers_sorted]

# Пример использования функции для регистрации маршрутов
get_routers(app)
