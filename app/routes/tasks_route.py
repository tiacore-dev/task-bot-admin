from fastapi import APIRouter, HTTPException, Depends
from app.database.models import Task
from app.pydantic_models.task_schemas import TaskCreateSchema, TaskSchema
from app.handlers.auth import get_current_admin

admin_tasks_router = APIRouter(prefix="/admin/tasks", tags=["admin_tasks"])

# 📌 Создание нового задания (только для админов)


@admin_tasks_router.post("/", response_model=TaskSchema)
async def create_task(task_data: TaskCreateSchema, admin=Depends(get_current_admin)):
    task = await Task.create(**task_data.dict(), creator_id=admin.admin_id)
    return TaskSchema.model_validate(task)

# 📌 Получение списка всех заданий


@admin_tasks_router.get("/", response_model=list[TaskSchema])
async def get_tasks():
    tasks = await Task.all()
    return [TaskSchema.model_validate(task) for task in tasks]

# 📌 Обновление задания


@admin_tasks_router.put("/{task_id}", response_model=TaskSchema)
async def update_task(task_id: str, task_data: TaskCreateSchema, admin=Depends(get_current_admin)):
    task = await Task.get_or_none(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await task.update_from_dict(task_data.dict())
    await task.save()
    return TaskSchema.model_validate(task)

# 📌 Удаление задания


@admin_tasks_router.delete("/{task_id}")
async def delete_task(task_id: str, admin=Depends(get_current_admin)):
    task = await Task.get_or_none(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await task.delete()
    return {"message": "Task deleted"}
