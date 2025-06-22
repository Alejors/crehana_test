from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum as SQLAEnum
from sqlalchemy.orm import relationship

from app.domain.entities import Task
from .timemixin import TimestampMixin
from app.infrastructure.db import Base
from app.domain.priorities import TaskPriority


class TaskModel(TimestampMixin, Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    task_list_id = Column(Integer, ForeignKey("task_lists.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    priority = Column(SQLAEnum(TaskPriority), default=TaskPriority.medium)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    task_list = relationship("TaskListModel", back_populates="tasks")
    assigned_user = relationship("UserModel", foreign_keys=[assigned_user_id])

    @staticmethod
    def from_entity(entity: Task) -> "TaskModel":
        return TaskModel(
            id=entity.id if entity.id else None,
            description=entity.description,
            task_list_id=entity.task_list_id,
            is_completed=entity.is_completed,
            priority=entity.priority,
            assigned_user_id=entity.assigned_user_id
        )

    def to_entity(self) -> Task:
        return Task(
            id=self.id,
            description=self.description,
            task_list_id=self.task_list_id,
            is_completed=self.is_completed,
            priority=self.priority,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
            assigned_user_id=self.assigned_user_id,
            assigned_user_email=self.assigned_user.email if self.assigned_user else None
        )
