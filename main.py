from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.importer.download1c import receive_json_1c
from config.settings import app, templates
from api.auth.routes.users import router as users_router
from api.auth.routes.roles import router as roles_router
from api.auth.routes.login import router as login_router
from api.dict.routes.currency import router as currency_router
from api.dict.routes.country import router as country_router
from config.db import get_db

app.include_router(login_router, tags=["Авторизация"])
app.include_router(users_router, prefix="/users", tags=["Пользователи"])
app.include_router(roles_router, prefix="/roles", tags=["Роли и права доступа"])
app.include_router(currency_router, prefix="/currency", tags=["Валюта"])
app.include_router(country_router, prefix="/country", tags=["Страны"])


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
