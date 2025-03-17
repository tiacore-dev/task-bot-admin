from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from app.database.models import Task
from app.pydantic_models.task_schemas import TaskCreateSchema, TaskSchema, TaskUpdateSchema, TaskResponseSchema
from app.handlers.auth import get_current_user

admin_tasks_router = APIRouter(prefix="/admin/tasks", tags=["admin_tasks"])

# 📌 Создание нового задания (только для админов)


@admin_tasks_router.post("/", response_model=TaskResponseSchema)
async def create_task(task_data: TaskCreateSchema, admin=Depends(get_current_user)):
    if task_data.reward <= 0:
        raise HTTPException(
            status_code=400, detail="Вознаграждение должно быть положительным числом")

    task = await Task.create(creator_id=admin.get('admin_id'), **task_data.model_dump())
    return TaskResponseSchema(task_id=task.task_id)


# 📌 Получение списка всех заданий
@admin_tasks_router.get("/", response_model=list[TaskSchema])
async def get_tasks():
    # ✅ Получаем список словарей вместо объектов модели
    tasks = await Task.all().values()
    return [TaskSchema(**task) for task in tasks]


# 📌 Обновление задания
@admin_tasks_router.patch("/{task_id}", response_model=TaskResponseSchema)
async def update_task(task_id: UUID, task_data: TaskUpdateSchema, admin=Depends(get_current_user)):
    task = await Task.get_or_none(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задание не найдено")

    updated_fields = task_data.dict(
        exclude_unset=True)  # Исключаем None-значения
    await task.update_from_dict(updated_fields)
    await task.save()

    return TaskResponseSchema(task_id=task.task_id)


# 📌 Удаление задания
@admin_tasks_router.delete("/{task_id}")
async def delete_task(task_id: UUID, admin=Depends(get_current_user)):
    task = await Task.get_or_none(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задание не найдено")

    await task.delete()
    return {"message": "Задание удалено"}
