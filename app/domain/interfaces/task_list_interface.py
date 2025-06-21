from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import TaskList
from app.domain.schemas import TaskListCreate, TaskListUpdate


class ITaskListRepository(ABC):
    @abstractmethod
    def get(self, id: int) -> Optional[TaskList]:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def create(self, task_list_in: TaskListCreate) -> TaskList:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def update(self, id: int, task_list_in: TaskListUpdate) -> TaskList:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def list_all(self) -> List[TaskList]:
        raise NotImplementedError("Method Not Implemented")
