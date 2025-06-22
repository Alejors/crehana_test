import pytest
from unittest.mock import AsyncMock

from app.usecases import TaskListUsecase
from app.domain.entities import TaskList, Task
from app.exceptions import TaskListDeletionError


@pytest.mark.asyncio
async def test_get_lists(mock_task_list_repo):
    mock_task_list_repo.list_all = AsyncMock(
        return_value=[
            TaskList(id=1, name="Lista 1"),
            TaskList(id=2, name="Lista 2"),
        ]
    )

    usecase = TaskListUsecase(task_list_repository=mock_task_list_repo)

    result = await usecase.get_lists()

    assert len(result) == 2
    assert result[0].name == "Lista 1"
    mock_task_list_repo.list_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_list_by_id(mock_task_list_repo):
    mock_task_list_repo.get = AsyncMock(return_value=TaskList(id=1, name="Lista 1"))

    usecase = TaskListUsecase(task_list_repository=mock_task_list_repo)

    result = await usecase.get_list_by_id(1)

    assert result.id == 1
    assert result.name == "Lista 1"
    mock_task_list_repo.get.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_create_list(mock_task_list_repo):
    list_name = "Lista Creada"
    mock_task_list_repo.create = AsyncMock(return_value=TaskList(id=1, name=list_name))

    usecase = TaskListUsecase(task_list_repository=mock_task_list_repo)

    task_list = TaskList(name=list_name)

    result = await usecase.create_list(task_list)

    assert result.id == 1
    assert result.name == list_name
    mock_task_list_repo.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_list(mock_task_list_repo):
    updated_name = "Lista Actualizada"
    mock_task_list_repo.update = AsyncMock(
        return_value=TaskList(id=2, name=updated_name)
    )

    usecase = TaskListUsecase(task_list_repository=mock_task_list_repo)

    task_list = TaskList(name=updated_name)

    result = await usecase.update_list(2, task_list)

    assert result.id == 2
    assert result.name == updated_name
    mock_task_list_repo.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_none(mock_task_list_repo):
    # Probamos que cuando se intenta hacer
    # una actualización con todos los campos vacíos,
    # el caso de uso lo detiene.
    usecase = TaskListUsecase(task_list_repository=mock_task_list_repo)

    task_list = TaskList(name=None)

    result = await usecase.update_list(2, task_list)

    assert result is None
    mock_task_list_repo.update.assert_not_called()


@pytest.mark.asyncio
async def test_delete_list(mock_task_list_repo):
    mock_task_list_repo.get = AsyncMock(return_value=TaskList(id=1, name="Lista 1"))
    mock_task_list_repo.delete = AsyncMock(return_value=True)

    usecase = TaskListUsecase(task_list_repository=mock_task_list_repo)

    result = await usecase.delete_list(2)

    assert result is True
    mock_task_list_repo.delete.assert_awaited_once_with(2)


@pytest.mark.asyncio
async def test_delete_blocked(mock_task_list_repo):
    mock_task_list_repo.get = AsyncMock(
        return_value=TaskList(
            id=1, name="Lista 1", tasks=[Task(id=1, task_list_id=1, description="x")]
        )
    )

    usecase = TaskListUsecase(task_list_repository=mock_task_list_repo)

    with pytest.raises(TaskListDeletionError) as exc_info:
        await usecase.delete_list(2)

    assert str(exc_info.value) == "Cannot Delete a List with Active Tasks."
    mock_task_list_repo.delete.assert_not_called()
