from typing import List

from app.domain.entities import Task
from app.domain.interfaces import (
    ITaskRepository,
    ITaskListRepository,
    IUserRepository,
    IMailingService,
)
from app.domain.utils import extract_non_null_fields


class TaskUsecase:
    def __init__(
        self,
        task_repository: ITaskRepository,
        task_list_repository: ITaskListRepository,
        user_repository: IUserRepository,
        mailing_service: IMailingService,
    ):
        self.task_repository = task_repository
        self.task_list_repository = task_list_repository
        self.user_repository = user_repository
        self.mailing_service = mailing_service

    async def get(self, id: int) -> Task:
        return await self.task_repository.get(id)
    
    async def _check_user(self, task_in: Task) -> Task:
        user_email = task_in.assigned_user_email
        if user_email:
            user_exists = await self.user_repository.get_user_by_email(user_email)
            if not user_exists:
                self.mailing_service.sendmail(user_email)
            else:
                task_in.assigned_user_id = user_exists.id
        return task_in

    async def create(self, task_in: Task) -> Task:
        task_in = await self._check_user(task_in)

        return await self.task_repository.create(task_in)

    async def update(self, id: int, task_in: Task) -> Task:
        task_in = await self._check_user(task_in)
        update_values = extract_non_null_fields(task_in)
        if not update_values:
            return None

        return await self.task_repository.update(id, update_values)

    async def delete(self, id: int) -> bool:
        return await self.task_repository.delete(id)

    async def list_by_task_list(
        self, task_list_id: int, filters: dict = None
    ) -> tuple[List[Task], int]:
        task_list = await self.task_list_repository.get(task_list_id)
        tasks = await self.task_repository.list_by_task_list(
            task_list_id, filters=filters
        )
        return tasks, task_list.completion_percentage
