from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from app.domain.priorities import TaskPriority


@dataclass
class Task:
    description: str
    task_list_id: int
    is_completed: bool = False
    priority: TaskPriority = TaskPriority.medium
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    id: Optional[int] = None
    assigned_user_email: Optional[str] = None
    assigned_user_id: Optional[int] = None
