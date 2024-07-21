from fastapi import Request
from config.settings import app, templates

# root
@app.get("/", tags=["Страницы"])
async def home_page(request: Request):
    data = {"request": request, "title": 'Главная Expeditor'}
    return templates.TemplateResponse("index.html", data)

@app.get("/login", tags=["Страницы"])
async def login_page(request: Request):
    data = {"request": request, "title": 'Авторизация'}
    return templates.TemplateResponse("login.html", data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
