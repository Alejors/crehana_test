from typing import Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")


class ApiResponse(GenericModel, Generic[T]):
    message: str
    data: T

class TasksList(GenericModel, Generic[T]):
    completion_percentage: int
    tasks: T
