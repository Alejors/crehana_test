from pydantic import BaseModel
from typing import Optional

from app.domain.entities import Task
from app.domain.priorities import TaskPriority


class TaskBase(BaseModel):
    description: str
    task_list_id: int | None = None
    is_completed: bool = False
    priority: TaskPriority = TaskPriority.medium
    
    def to_entity(self) -> Task:
        return Task(
            self.description,
            self.task_list_id,
            self.is_completed,
            self.priority
        )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[TaskPriority] = None
    
    def to_entity(self) -> Task:
        return Task(
            self.description,
            None,
            self.is_completed,
            self.priority
        )


class TaskOut(TaskBase):
    id: int
    
    @classmethod
    def from_entity(cls, entity: Task) -> "TaskOut":
        return cls(
            id=entity.id,
            description=entity.description,
            task_list_id=entity.task_list_id,
            is_completed=entity.is_completed,
            priority=entity.priority
        )
