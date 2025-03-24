from uuid import UUID
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.database.models import User, TaskAssignment
from app.pydantic_models.user_schemas import UserSchema
from app.handlers.auth import get_current_user

user_router = APIRouter(prefix="/api/users", tags=["admin_tasks"])


@user_router.get("", response_model=List[UserSchema])
async def get_users(admin=Depends(get_current_user)):
    users = await User.all().values()
    return [
        UserSchema(**user)
        for user in users
    ]


@user_router.get("/{user_id}")
async def get_user_detail(user_id: UUID, admin=Depends(get_current_user)):
    user = await User.get_or_none(user_id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # 📌 Задания, которые пользователь взял в работу
    assigned_tasks = await TaskAssignment.filter(user=user).prefetch_related("task")

    return {
        "user_id": user.user_id,
        "username": user.username,
        "created_at": user.created_at,
        "tasks": [
            {
                "task_id": assignment.task.task_id,
                "task_name": assignment.task.task_name,
                "status": assignment.status,  # 🟢 Статус именно из `TaskAssignment`
                "assigned_profile": assignment.assigned_profile_id,
                "submitted_at": assignment.submitted_at,
            }
            for assignment in assigned_tasks
        ],
    }
