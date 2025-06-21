from typing import Optional, List
from datetime import datetime
from .task import Task


class TaskList:

    def __init__(
        self,
        *,
        name: str,
        tasks: Optional[List[Task]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        id: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.tasks = tasks or []
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    @property
    def completion_percentage(self) -> int:
        if not self.tasks:
            return 100
        completed = sum(1 for task in self.tasks if task.is_completed)
        return round((completed / len(self.tasks)) * 100)
