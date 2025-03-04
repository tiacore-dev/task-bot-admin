from pathlib import Path
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

frontend_router = APIRouter(tags=["frontend"])

# 🟢 Указываем путь к шаблонам
BASE_DIR = Path(__file__).parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "frontend" / "templates"))


@frontend_router.get("/", response_class=HTMLResponse)
async def serve_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@frontend_router.get("/admin", response_class=HTMLResponse)
async def serve_tasks(request: Request):
    return templates.TemplateResponse("tasks.html", {"request": request})
