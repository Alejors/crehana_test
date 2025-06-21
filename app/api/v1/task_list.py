from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from app.usecases import TaskListUsecase
from app.domain.utils import verify_token
from app.exceptions import TaskListDeletionError
from app.domain.schemas import TaskListCreate, TaskListUpdate, TaskListOut


def create_task_lists_route(task_list_usecase: TaskListUsecase) -> APIRouter:

    router: APIRouter = APIRouter(dependencies=[Depends(verify_token)])

    @router.get("/task-lists", response_model=List[TaskListOut])
    async def get_task_lists() -> List[TaskListOut]:
        task_lists = await task_list_usecase.get_lists()
        return [
            TaskListOut.from_entity(task_list) for task_list in task_lists if task_list
        ]

    @router.get("/task-lists/{task_list_id}", response_model=TaskListOut)
    async def get_task_by_id(task_list_id: int):
        task_list = await task_list_usecase.get_list_by_id(task_list_id)
        if not task_list:
            raise HTTPException(status_code=404, detail="Task List Not Found")
        return TaskListOut.from_entity(task_list)

    @router.post(
        "/task-lists", status_code=status.HTTP_201_CREATED
    )  # TODO: crear una interfaz que mapee message: str, data: T
    async def create_task_list(payload: TaskListCreate):
        try:
            task_created = await task_list_usecase.create_list(payload.to_entity())
            return {
                "message": "Task List Created",
                "data": TaskListOut.from_entity(task_created),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.put("/task-lists/{task_list_id}")
    async def update_task_list(task_list_id: int, payload: TaskListUpdate):
        try:
            task_updated = await task_list_usecase.update_list(
                task_list_id, payload.to_entity()
            )
            return {
                "message": "Task List Updated",
                "data": TaskListOut.from_entity(task_updated),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.delete("/task-lists/{task_list_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_task_list(task_list_id: int):
        try:
            task_deleted = await task_list_usecase.delete_list(task_list_id)
            if not task_deleted:
                raise HTTPException(
                    status_code=404, detail="Task List Could Not Be Deleted"
                )
            return
        except HTTPException:
            raise
        except TaskListDeletionError:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
