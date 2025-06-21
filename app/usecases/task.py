from app.domain.entities import Task
from app.domain.interfaces import ITaskRepository
from app.domain.utils import extract_non_null_fields


class TaskUsecase:
    def __init__(self, task_repository: ITaskRepository):
        self.task_repository = task_repository
        
    async def get(self, id: int) -> Task:
        return await self.task_repository.get(id)

    async def create(self, task_in: Task) -> Task:
        return await self.task_repository.create(task_in)
    
    async def update(self, id: int, task_in: Task) -> Task:
        update_values = extract_non_null_fields(task_in)
        if not update_values:
            return None
        
        return await self.task_repository.update(id, update_values)
    
    async def delete(self, id: int) -> bool:
        return await self.task_repository.delete(id)
    
    async def list_by_task_list(self, task_list_id: int, filters: dict = None):
        return await self.task_repository.list_by_task_list(task_list_id, filters=filters)
