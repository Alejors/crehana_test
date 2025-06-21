from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import TaskList


class ITaskListRepository(ABC):
    @abstractmethod
    def get(self, id: int) -> Optional[TaskList]:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def create(self, task_list_in: TaskList) -> TaskList:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def update(self, id: int, task_list_in: TaskList) -> TaskList:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def delete(self, id: int) -> bool:
        raise NotImplementedError("Method Not Implemented")

    @abstractmethod
    def list_all(self) -> List[TaskList]:
        raise NotImplementedError("Method Not Implemented")
