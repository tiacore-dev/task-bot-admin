from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from app.database.models import TaskStatus, AdminUser, UserRole, TaskType, TaskPlatform
from app.handlers.auth import get_current_user


admin_meta_router = APIRouter(prefix="/api/meta", tags=["admin_meta"])


@admin_meta_router.get("/task_statuses")
@cache(expire=3600)  # Кэшируем на 1 час
async def get_task_statuses(admin=Depends(get_current_user)):
    statuses = await TaskStatus.all()
    return [{"status_id": s.status_id, "name": s.status_name} for s in statuses]


@admin_meta_router.get("/task_types")
@cache(expire=3600)
async def get_task_types(admin=Depends(get_current_user)):
    types = await TaskType.all()
    return [{"task_type_id": t.task_type_id, "name": t.task_type_name} for t in types]


@admin_meta_router.get("/user_roles")
@cache(expire=3600)
async def get_user_roles(admin=Depends(get_current_user)):
    roles = await UserRole.all()
    return [{"role_id": r.role_id, "name": r.role_name} for r in roles]


@admin_meta_router.get("/platforms")
@cache(expire=3600)
async def get_task_platforms():
    platforms = await TaskPlatform.all()
    return [{"platform_id": p.platform_id, "name": p.platform_name} for p in platforms]


@admin_meta_router.get("/admin_users")
async def get_admin_users(admin=Depends(get_current_user)):  # Только для админов
    admins = await AdminUser.all()
    return [{"admin_id": a.admin_id, "username": a.username} for a in admins]
