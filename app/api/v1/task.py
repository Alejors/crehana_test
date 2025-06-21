from typing import List
from fastapi import APIRouter, HTTPException, status, Request

from app.usecases import TaskUsecase
from app.domain.schemas import TaskCreate, TaskUpdate, TaskOut


def create_task_route(task_usecase: TaskUsecase) -> APIRouter:

    router: APIRouter = APIRouter()

    @router.get("/task/{task_id}", response_model=List[TaskOut])
    async def get_task(task_id: int) -> List[TaskOut]:
        task = await task_usecase.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task Not Found")
        return TaskOut.from_entity(task)
    
    @router.get("/task-lists/{task_list_id}/tasks", response_model=List[TaskOut])
    async def get_tasks_by_list_id(task_list_id: int, request: Request):
        filters = dict(request.query_params)
        tasks = await task_usecase.list_by_task_list(task_list_id, filters)
        if not tasks:
            raise HTTPException(status_code=404, detail="Tasks Not Found for this List")
        return [TaskOut.from_entity(task) for task in tasks if task]
    
    @router.post("/task-lists/{task_list_id}/tasks", status_code=status.HTTP_201_CREATED)
    async def create_task(task_list_id: int, payload: TaskCreate):
        payload.task_list_id = task_list_id
        try:
            task_created = await task_usecase.create(payload.to_entity())
            return {"message": "Task List Created", "data": TaskOut.from_entity(task_created)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @router.put("/task/{task_id}")
    async def update_task(task_id: int, payload: TaskUpdate):
        try:
            task_updated = await task_usecase.update(task_id, payload.to_entity())
            return {"message": "Task Updated", "data": TaskOut.from_entity(task_updated)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @router.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_task(task_id: int):
        try:
            task_deleted = await task_usecase.delete(task_id)
            if not task_deleted:
                raise HTTPException(status_code=404, detail="Task Could Not Be Deleted")
            return
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
