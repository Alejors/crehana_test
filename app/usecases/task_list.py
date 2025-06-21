from app.domain.entities import TaskList
from app.exceptions import TaskListDeletionError
from app.domain.utils import extract_non_null_fields
from app.domain.interfaces import ITaskListRepository


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
        update_dict = extract_non_null_fields(task_list)
        if not update_dict:
            return None
        return await self.task_list_repository.update(task_list_id, update_dict)
    
    async def delete_list(self, task_list_id: int) -> bool:
        task_list = await self.task_list_repository.get(task_list_id)
        if any(not task.is_completed for task in task_list.tasks):
            raise TaskListDeletionError()
        return await self.task_list_repository.delete(task_list_id)
