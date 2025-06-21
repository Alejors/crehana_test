from enum import Enum


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
