from datetime import datetime
from sqlalchemy import select
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.entities import TaskList
from app.domain.interfaces import ITaskListRepository
from app.infrastructure.db.models.task_list import TaskListModel


class SQLAlchemyTaskListRepository(ITaskListRepository):

    def __init__(self, session: Session):
        self.db = session

    async def _find_by_id(self, session, id: int):
        stmt = select(TaskListModel).where(
            TaskListModel.id == id,
            TaskListModel.deleted_at.is_(None),
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, task_list: TaskList) -> TaskList:
        async with self.db() as session:
            task_list_model = TaskListModel.from_entity(task_list)
            session.add(task_list_model)
            await session.commit()
            await session.refresh(task_list_model)
            return task_list_model.to_entity()

    async def get(self, id: int) -> Optional[TaskList]:
        async with self.db() as session:
            task_list_model = await self._find_by_id(session, id)
            return task_list_model.to_entity() if task_list_model else None

    async def update(self, id: int, dict_values: dict) -> TaskList:
        async with self.db() as session:
            task_list_model = await self._find_by_id(session, id)
            if not task_list_model:
                return None

            for key, value in dict_values.items():
                setattr(task_list_model, key, value)

            await session.commit()
            await session.refresh(task_list_model)

            return task_list_model.to_entity()

    async def delete(self, id: int) -> bool:
        async with self.db() as session:
            task_list_model = await self._find_by_id(session, id)
            if not task_list_model:
                return False

            task_list_model.deleted_at = datetime.now()
            await session.commit()

            return True

    async def list_all(self) -> List[TaskList]:
        async with self.db() as session:
            stmt = select(TaskListModel).where(TaskListModel.deleted_at.is_(None))
            result = await session.execute(stmt)
            task_list_models = result.scalars().all()
            return [
                tasklistmodel.to_entity()
                for tasklistmodel in task_list_models
                if tasklistmodel
            ]
