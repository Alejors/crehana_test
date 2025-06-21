from pydantic import BaseModel
from typing import Optional
from app.domain.priorities import TaskPriority


class TaskBase(BaseModel):
    description: str
    task_list_id: int
    is_completed: bool = False
    priority: TaskPriority = TaskPriority.medium


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[TaskPriority] = None


class TaskOut(TaskBase):
    id: int
