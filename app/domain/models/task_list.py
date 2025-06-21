from sqlalchemy import Column, Integer, String
from app.infrastructure import Base

class TaskList(Base):
    __tablename__ = "task_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
