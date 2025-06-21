from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Task
from app.domain.schemas import TaskCreate, TaskUpdate


class ITaskRepository(ABC):
    @abstractmethod
    def get(self, id: int) -> Optional[Task]:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def create(self, task_in: TaskCreate) -> Task:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def update(self, id: int, task_in: TaskUpdate) -> Task:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def list_by_task_list(
        self, task_list_id: int, *, filters: dict = None
    ) -> List[Task]:
        raise NotImplementedError("Method Not Implemented")
