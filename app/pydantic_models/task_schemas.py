from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, UUID4


# Платформа для заданий
class TaskPlatformSchema(BaseModel):
    platform_id: UUID4
    name: str


class TaskTypeSchema(BaseModel):
    task_type_id: str
    name: str


class TaskStatusSchema(BaseModel):
    status_id: str
    name: str

# Задание (отображение)


class TaskSchema(BaseModel):
    task_id: UUID4
    creator_id: UUID4
    platform_id: UUID4
    task_type_id: str
    task_name: str  # 🔥 Новое поле
    description: str
    reward: Decimal
    verification_type: str
    status_id: str

# Создание задания


class TaskResponseSchema(BaseModel):
    task_id: UUID4


class TaskCreateSchema(BaseModel):
    # creator_id: UUID4
    platform_id: UUID4
    task_type_id: str
    task_name: str  # 🔥 Новое поле
    description: str
    reward: Decimal
    verification_type: str
    status_id: str

# Обновление задания


class TaskUpdateSchema(BaseModel):
    task_name: Optional[str] = None  # 🔥 Новое поле
    description: Optional[str] = None
    reward: Optional[Decimal] = None
    status_id: Optional[str] = None
