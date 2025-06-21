from pydantic import BaseModel

from app.domain.entities import TaskList


class TaskListBase(BaseModel):
    name: str
    
    def to_entity(self):
        return TaskList(name=self.name)


class TaskListCreate(TaskListBase):
    pass


class TaskListUpdate(TaskListBase):
    pass


class TaskListOut(TaskListBase):
    id: int
    completion_percentage: int
    
    @classmethod
    def from_entity(cls, entity: TaskList):
        return cls(
            id=entity.id,
            name=entity.name,
            completion_percentage=entity.completion_percentage
        )
