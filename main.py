from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.imports.data1c import receive_json_1c
from api.imports.dicts_rw.data_rw import load_rw_json
from api.imports.dislocation import load_dislocation
from config.settings import app, templates
from config.db import get_db


# first
@app.post("/1c", tags=["Импорт данных"])
async def post_1c(request: Request, db: AsyncSession = Depends(get_db)):
    return await receive_json_1c(request, db)


@app.post("/load_dicts_rw", tags=["Импорт данных"])
async def post_rw(request: Request, db: AsyncSession = Depends(get_db)):
    return await load_rw_json(request, db)


@app.post("/load_dislocation", tags=["Импорт данных"])
async def post_disclocation(request: Request, db: AsyncSession = Depends(get_db)):
    return await load_dislocation(request, db)


# root
@app.get("/", tags=["Страницы"])
async def read_root(request: Request):
    data = {"request": request, "title": 'Главная Expeditor'}
    return templates.TemplateResponse("index.html", data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
