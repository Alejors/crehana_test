import pytest
from unittest.mock import AsyncMock

from app.domain.entities import Task, TaskList, User
from app.usecases import TaskUsecase


TASK1 = Task(description="test-1", task_list_id=1, id=1, is_completed=True)
TASK2 = Task(description="updated-2", task_list_id=1, id=2, is_completed=False)

@pytest.mark.asyncio
async def test_get_task(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service):
    mock_task_repo.get = AsyncMock(return_value=TASK1)
    
    usecase = TaskUsecase(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service)
    
    result = await usecase.get(1)
    
    assert isinstance(result, Task)
    assert result.id == 1
    assert result.description == "test-1"
    
@pytest.mark.asyncio
async def test_create_task(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service):
    mock_task_repo.create = AsyncMock(return_value=TASK1)
    
    usecase = TaskUsecase(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service)
    
    # No le pasamos el id
    task_in = Task(description="test-1", task_list_id=1)
    
    result = await usecase.create(task_in)
    
    assert isinstance(result, Task)
    assert result.id == 1
    
@pytest.mark.asyncio
async def test_create_task_with_assignee(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service):
    mock_task_repo.create = AsyncMock(return_value=TASK1)
    mock_user_repo.get_user_by_email = AsyncMock(return_value=User(id=1, email="test@test.com", password="abc123"))
    
    usecase = TaskUsecase(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service)
    
    task_in = Task(description="test-1", task_list_id=1, assigned_user_email="test@test.com")
    
    result = await usecase.create(task_in)
    
    assert isinstance(result, Task)
    mock_user_repo.get_user_by_email.assert_called_once()

@pytest.mark.asyncio
async def test_create_task_with_inexistent_assignee(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service):
    mock_task_repo.create = AsyncMock(return_value=TASK1)
    mock_user_repo.get_user_by_email = AsyncMock(return_value=None)
    
    usecase = TaskUsecase(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service)
    
    task_in = Task(description="test-1", task_list_id=1, assigned_user_email="test@test.com")
    
    result = await usecase.create(task_in)
    
    assert isinstance(result, Task)
    mock_user_repo.get_user_by_email.assert_called_once()
    mock_mailing_service.sendmail.assert_called_once()


@pytest.mark.asyncio
async def test_update_task(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service):
    mock_task_repo.update = AsyncMock(return_value=TASK2)
    
    usecase = TaskUsecase(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service)
    
    task_in = Task(description="updated-2", task_list_id=None)
    
    result = await usecase.update(2, task_in)
    
    assert result.id == 2
    assert result.description == "updated-2"
    mock_task_repo.update.assert_called_once()
    mock_task_repo.update.assert_awaited_once()
    
@pytest.mark.asyncio
async def test_update_none(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service):    
    usecase = TaskUsecase(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service)
    
    # Cuando llega un DTO vacío, 
    # se instancia una clase completamente vacía 
    # (AKA: llena de None's)
    task_in = Task(description=None, task_list_id=None, is_completed=None, priority=None)
    
    result = await usecase.update(2, task_in)
    
    assert result == None
    mock_task_repo.update.assert_not_called()
    
@pytest.mark.asyncio
async def test_delete_task(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service):
    mock_task_repo.delete = AsyncMock(return_value=True)
    
    usecase = TaskUsecase(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service)
    
    result = await usecase.delete(1)
    
    assert result == True
    
@pytest.mark.asyncio
async def test_list_by_task_list(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service):
    # Generamos un listado de tasks que serán las tareas de la lista
    task_list = [TASK1, TASK2]
    mock_task_list_repo.get = AsyncMock(return_value=TaskList(name="test", tasks=task_list))
    
    # Indicamos que el mock repo traerá este mismo listado
    mock_task_repo.list_by_task_list = AsyncMock(return_value=task_list)
    
    usecase = TaskUsecase(mock_task_repo, mock_task_list_repo, mock_user_repo, mock_mailing_service)
    
    tasks, completion_percentage = await usecase.list_by_task_list(1)
    assert len(tasks) == 2
    # como el listado tiene 1 completa y otra no, 
    # validamos que al generar la entidad se obtiene un 50%
    assert completion_percentage == 50
    