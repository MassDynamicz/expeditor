import os, importlib
from fastapi import FastAPI, APIRouter
from config.utils import camel_to_kebab

# Словарь для сопоставления имен файлов с тегами
tag_mappings = {
    "auth": "Авторизация",
    "roles": "Роли и права доступа",
    "users": "Пользователи",
    "session": "Сессии",
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
    "service-type": "Виды услуг",
    "wagon": "Вагоны",
    "container": "Контейнеры",
    "etsng": "Грузы по ЕТСНГ",
    "gng": "Грузы по ГНГ",
    "operation": "Операции по Ж/Д",
    "territory": "Территории Ж/Д",
    "station": "Станции Ж/Д",
    "dislocation": "Дислокация",
    "orders-railway": "Заявки Ж/Д",
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

    for prefix, tag, router in routers:
        app.include_router(router, prefix=prefix, tags=[tag])
