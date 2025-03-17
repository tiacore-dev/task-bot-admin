import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from tortoise.contrib.fastapi import register_tortoise
from app.logger import setup_logger
from app.routes import register_routes
from app.config import Settings


def create_app() -> FastAPI:
    app = FastAPI(title="Tiacore CRM")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Или указать твой Netlify-домен
        allow_credentials=True,
        allow_methods=["*"],  # Разрешаем все методы
        allow_headers=["*"],  # Разрешаем все заголовки
    )

    app.state.settings = Settings()
    # Настраиваем кэш
    FastAPICache.init(InMemoryBackend())
    # Подключение Tortoise ORM
    register_tortoise(
        app,
        db_url=Settings.DATABASE_URL,
        modules={"models": ["app.database.models"]},
        add_exception_handlers=True,
    )

    setup_logger()

    # Регистрация маршрутов
    register_routes(app)

    # Раздача статических файлов
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    return app
