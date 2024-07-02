from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
<<<<<<< HEAD
from api.importer.download1c import receive_json_1c
from config.settings import app, templates
from api.auth.routes.users import router as users_router
from api.auth.routes.roles import router as roles_router
from api.auth.routes.login import router as login_router
from api.dict.routes.currency import router as currency_router
from api.dict.routes.country import router as country_router
=======
from api.imports.data1c import receive_json_1c
from config.settings import app, templates
from api.auth.routes.users import router as users_router
from api.auth.routes.roles import router as roles_router
from api.auth.routes.auth import router as login_router
from api.dict.Currency.routes import router as currency_router
from api.dict.Country.routes import router as country_router
from api.dict.Vat.routes import router as vat_router
from api.dict.Bank.routes import router as bank_router
from api.dict.Organization.routes import router as organization_router
from api.dict.Contractor.routes import router as contractor_router
from api.dict.Contract.routes import router as contract_router
from api.dict.BankAccount.routes import router as bank_account_router
from api.dict.BankAccountOrg.routes import router as bank_account_org_router
from api.dict.WagonType.routes import router as wagon_type_router
from api.dict.ServiceType.routes import router as service_type_router
from api.dict.Wagon.routes import router as wagon_router
from api.dict.Container.routes import router as container_router
from api.dict.Etsng.routes import router as etsng_router
from api.dict.Gng.routes import router as gng_router
from api.dict.Operation.routes import router as operation_router
from api.dict.Territory.routes import router as territory_router
from api.dict.Station.routes import router as station_router
>>>>>>> f474fef (Updated)
from config.db import get_db

app.include_router(login_router, tags=["Авторизация"])
app.include_router(users_router, prefix="/users", tags=["Пользователи"])
app.include_router(roles_router, prefix="/roles", tags=["Роли и права доступа"])
app.include_router(currency_router, prefix="/currency", tags=["Валюта"])
app.include_router(country_router, prefix="/country", tags=["Страны"])
<<<<<<< HEAD
=======
app.include_router(vat_router, prefix="/vat", tags=["НДС"])
app.include_router(bank_router, prefix="/bank", tags=["Банк"])
app.include_router(organization_router, prefix="/organization", tags=["Организация"])
app.include_router(contractor_router, prefix="/contractor", tags=["Контрагент"])
app.include_router(contract_router, prefix="/contract", tags=["Договор"])
app.include_router(bank_account_router, prefix="/banc_account", tags=["Банковские счет контрагентов"])
app.include_router(bank_account_org_router, prefix="/banc_account_org", tags=["Банковские счет организации"])
app.include_router(wagon_type_router, prefix="/wagon_type", tags=["Роды подвижного состава"])
app.include_router(service_type_router, prefix="/service_type", tags=["Виды услуг"])
app.include_router(wagon_router, prefix="/wagon", tags=["Вагоны"])
app.include_router(container_router, prefix="/container", tags=["Контейнеры"])
app.include_router(etsng_router, prefix="/etsng", tags=["Грузы по ЕТСНГ"])
app.include_router(gng_router, prefix="/gng", tags=["Грузы по ГНГ"])
app.include_router(operation_router, prefix="/operation", tags=["Операции по Ж/Д"])
app.include_router(territory_router, prefix="/territory", tags=["Территории Ж/Д"])
app.include_router(station_router, prefix="/station", tags=["Станции Ж/Д"])
>>>>>>> f474fef (Updated)


@app.post("/1c")
async def post_1c(request: Request, db: AsyncSession = Depends(get_db)):
    return await receive_json_1c(request, db)


# root
@app.get("/", tags=["Страницы"])
async def read_root(request: Request):
    data = {"request": request, "title": 'Главная Expeditor'}
    return templates.TemplateResponse("index.html", data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
