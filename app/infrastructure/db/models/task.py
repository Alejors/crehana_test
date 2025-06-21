from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum as SQLAEnum
from app.infrastructure.db import Base
from app.domain.priorities import TaskPriority
from .timemixin import TimestampMixin


class TaskModel(TimestampMixin, Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    task_list_id = Column(Integer, ForeignKey("task_lists.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    priority = Column(SQLAEnum(TaskPriority), default=TaskPriority.medium)
