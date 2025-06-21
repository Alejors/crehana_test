from sqlalchemy import Column, Integer, String
from app.infrastructure.db import Base
from .timemixin import TimestampMixin
from app.domain.entities import TaskList


class TaskListModel(TimestampMixin, Base):
    __tablename__ = "task_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    
    @staticmethod
    def from_entity(task_list: TaskList):
        return TaskListModel(
            id=task_list.id if task_list.id else None,
            name = task_list.name,
        )
        
    def to_entity(self) -> TaskList:
        return TaskList(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at
        )