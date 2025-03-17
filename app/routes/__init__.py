from .tasks_route import admin_tasks_router
from .auth_route import auth_router
from .frontend_route import frontend_router
from .get_info_route import admin_meta_router


def register_routes(app):
    app.include_router(admin_tasks_router)
    app.include_router(auth_router)
    app.include_router(frontend_router)
    app.include_router(admin_meta_router)
