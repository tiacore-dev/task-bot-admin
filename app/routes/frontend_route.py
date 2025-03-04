from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

frontend_router = APIRouter(tags=["frontend"])

templates = Jinja2Templates(directory="app/templates")


@frontend_router.get("/login", response_class=HTMLResponse)
async def serve_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@frontend_router.get("/admin", response_class=HTMLResponse)
async def serve_tasks(request: Request):
    return templates.TemplateResponse("tasks.html", {"request": request})


@frontend_router.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
