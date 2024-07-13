import os
import importlib
from fastapi import FastAPI, APIRouter

# Словарь для сопоставления имен файлов с тегами
tag_mappings = {
    "auth": "Авторизация",
    "roles": "Роли и права доступа",
    "users": "Пользователи",
    "currency": "Валюта",
    "country": "Страны",
    "vat": "НДС",
    "bank": "Банк",
    "organization": "Организация",
    "contractor": "Контрагент",
    "contract": "Договор",
    "bankaccount": "Банковские счета контрагентов",
    "bankaccountorg": "Банковские счета организации",
    "wagontype": "Роды подвижного состава",
    "servicetype": "Виды услуг",
    "wagon": "Вагоны",
    "container": "Контейнеры",
    "etsng": "Грузы по ЕТСНГ",
    "gng": "Грузы по ГНГ",
    "operation": "Операции по Ж/Д",
    "territory": "Территории Ж/Д",
    "station": "Станции Ж/Д",
    "dislocation": "Дислокация",
    "order": "Заявки Ж/Д",
    "order_route": "Заявки Ж/Д",
    "order_transport": "Заявки Ж/Д",
    "order_provider": "Заявки Ж/Д",
    "rwcode": "Ж/Д коды",
    "subcode": "Подкоды",
}

# Словарь исключений для префиксов
prefix_exceptions = ["auth"]


def get_routers(app: FastAPI):
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
                if folder_name in prefix_exceptions:
                    prefix = ""
                else:
                    prefix = f"/{folder_name.lower()}"
                tag = tag_mappings.get(folder_name.lower(), folder_name.replace("_", " ").title())
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
                        if file_name in prefix_exceptions:
                            prefix = ""
                        else:
                            prefix = f"/{file_name.lower()}"
                        tag = tag_mappings.get(file_name.lower(), file_name.replace("_", " ").title())
                        routers.append((prefix, tag, router))

    for prefix, tag, router in routers:
        app.include_router(router, prefix=prefix, tags=[tag])
