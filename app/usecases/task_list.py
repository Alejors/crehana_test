from app.domain.interfaces import ITaskListRepository
from app.domain.entities import TaskList


class TaskListUsecase:
    def __init__(self, task_list_repository: ITaskListRepository):
        self.task_list_repository = task_list_repository
        
    async def get_lists(self) -> list[TaskList]:
        return await self.task_list_repository.list_all()
    
    async def get_list_by_id(self, id: int) -> TaskList:
        return await self.task_list_repository.get(id)
    
    async def create_list(self, task_list: TaskList) -> TaskList:
        return await self.task_list_repository.create(task_list)
    
    async def update_list(self, task_list_id: int, task_list: TaskList) -> TaskList:
        return await self.task_list_repository.update(task_list_id, task_list)
    
    async def delete_list(self, task_list_id: int) -> bool:
        return await self.task_list_repository.delete(task_list_id)
