from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    task_list_id = Column(Integer, ForeignKey("task_lists.id"))