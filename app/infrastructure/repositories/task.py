from datetime import datetime
from sqlalchemy import select
from typing import List, Optional
from sqlalchemy.orm import Session, selectinload

from app.domain.entities import Task
from app.domain.interfaces import ITaskRepository
from app.infrastructure.db.models.task import TaskModel
from app.infrastructure.utils.sqlalchemy_filters_parser import parse_filters


class SQLAlchemyTaskRepository(ITaskRepository):

    def __init__(
        self,
        session: Session,
    ):
        self.db = session

    async def _find_by_id(self, session, id: int):
        stmt = (
            select(TaskModel)
            .options(selectinload(TaskModel.assigned_user))
            .where(
                TaskModel.id == id,
                TaskModel.deleted_at.is_(None),
            )
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get(self, id: int) -> Optional[Task]:
        async with self.db() as session:
            task_model = await self._find_by_id(session, id)
            return task_model.to_entity() if task_model else None

    async def create(self, task_in: Task) -> Task:
        async with self.db() as session:
            task_model = TaskModel.from_entity(task_in)
            session.add(task_model)
            await session.commit()
            await session.refresh(task_model)
            return await self.get(task_model.id)

    async def update(self, task_id: int, update_values: dict) -> Task:
        async with self.db() as session:
            task_model = await self._find_by_id(session, task_id)
            if not task_model:
                return None

            for key, value in update_values.items():
                setattr(task_model, key, value)

            await session.commit()
            await session.refresh(task_model)

            return task_model.to_entity()

    async def delete(self, task_id: int) -> bool:
        async with self.db() as session:
            task_model = await self._find_by_id(task_id)
            if not task_model:
                return False

            task_model.deleted_at = datetime.now()
            await session.commit()

            return True

    async def list_by_task_list(
        self, task_list_id: int, *, filters: dict = None
    ) -> List[Task]:

        additional_filters = parse_filters(filters, TaskModel) if filters else True

        async with self.db() as session:
            stmt = (
                select(TaskModel)
                .options(selectinload(TaskModel.assigned_user))
                .where(
                    TaskModel.task_list_id == task_list_id,
                    TaskModel.deleted_at.is_(None),
                    additional_filters,
                )
            )

            result = await session.execute(stmt)
            tasks_models = result.scalars().all()
            return [task_model.to_entity() for task_model in tasks_models if task_model]
