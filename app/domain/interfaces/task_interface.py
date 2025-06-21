from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import Task


class ITaskRepository(ABC):
    @abstractmethod
    def get(self, id: int) -> Optional[Task]:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def create(self, task_in: Task) -> Task:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def update(self, id: int, update_values: dict) -> Task:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def delete(self, id: int) -> bool:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def list_by_task_list(
        self, task_list_id: int, *, filters: dict = None
    ) -> List[Task]:
        raise NotImplementedError("Method Not Implemented")
