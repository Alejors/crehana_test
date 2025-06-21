from sqlalchemy import Column, Integer, String
from app.infrastructure import Base
from .timemixin import TimestampMixin

class TaskList(TimestampMixin, Base):
    __tablename__ = "task_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
