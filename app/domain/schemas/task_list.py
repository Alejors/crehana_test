from pydantic import BaseModel


class TaskListBase(BaseModel):
    name: str


class TaskListCreate(TaskListBase):
    pass


class TaskListUpdate(TaskListBase):
    pass


class TaskListOut(TaskListBase):
    id: int
