import pytest
from fastapi import FastAPI
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from app.domain.entities import Task
from app.usecases import TaskUsecase
from app.api.v1 import create_task_route
from app.domain.utils import verify_token


TASK1 = Task(description="test-1", task_list_id=1, id=1, is_completed=True)
TASK2 = Task(description="updated-2", task_list_id=1, id=2, is_completed=False)


@pytest.fixture
def mock_usecase():
    return AsyncMock(spec=TaskUsecase)


@pytest.fixture
def client(mock_usecase, override_auth_dependency):
    app = FastAPI()
    router = create_task_route(mock_usecase)
    app.include_router(router, prefix="/api/v1")
    app.dependency_overrides[verify_token] = override_auth_dependency
    return TestClient(app)


def test_get_task(client, mock_usecase):
    mock_usecase.get.return_value = TASK1

    response = client.get("/api/v1/task/1")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "data" in data
    assert data["data"]["id"] == 1


def test_get_none_task(client, mock_usecase):
    mock_usecase.get.return_value = None

    response = client.get("/api/v1/task/1")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "data" not in data
    assert data["detail"] == "Task Not Found"


def test_get_tasks_by_list_no_filters(client, mock_usecase):
    mock_usecase.list_by_task_list.return_value = [[TASK1, TASK2], 50]

    response = client.get("/api/v1/task-lists/1/tasks")

    assert response.status_code == 200
    data = response.json()
    response_data = data["data"]
    assert "completion_percentage" in response_data
    assert response_data["completion_percentage"] == 50
    assert "tasks" in response_data
    assert len(response_data["tasks"]) == 2


def test_get_tasks_no_tasks(client, mock_usecase):
    mock_usecase.list_by_task_list.return_value = [[], 100]

    response = client.get("/api/v1/task-lists/1/tasks?priority=high")

    assert response.status_code == 404
    mock_usecase.list_by_task_list.assert_called_once_with(1, {"priority": "high"})


def test_create_task(client, mock_usecase):
    mock_usecase.create.return_value = TASK1

    payload = {"description": "test-1"}

    response = client.post("/api/v1/task-lists/1/tasks", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Task Created"
    assert data["data"]["description"] == TASK1.description


def test_create_raise_exception(client, mock_usecase):
    mock_usecase.create.side_effect = ValueError("some error")

    payload = {"description": "test-1"}

    response = client.post("/api/v1/task-lists/1/tasks", json=payload)

    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "some error"


def test_update_task(client, mock_usecase):
    mock_usecase.update.return_value = TASK2

    payload = {"description": "updated-2"}

    response = client.put("/api/v1/task/2", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task Updated"
    assert data["data"]["description"] == TASK2.description


def test_update_raise_exception(client, mock_usecase):
    mock_usecase.update.side_effect = ValueError("some error")

    payload = {"description": "updated-2"}

    response = client.put("/api/v1/task/2", json=payload)

    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "some error"


def test_delete_task_true(client, mock_usecase):
    mock_usecase.delete.return_value = True

    response = client.delete("/api/v1/task/2")

    assert response.status_code == 204
    # Validamos el response vacío
    assert response.content == b""


def test_delete_task_false(client, mock_usecase):
    mock_usecase.delete.return_value = False

    response = client.delete("/api/v1/task/2")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Task Could Not Be Deleted"


def test_delete_raise_exception(client, mock_usecase):
    mock_usecase.delete.side_effect = ValueError("some error")

    response = client.delete("/api/v1/task/2")

    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "some error"
