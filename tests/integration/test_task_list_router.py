import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from app.api.v1 import create_task_lists_route
from app.usecases import TaskListUsecase
from app.domain.entities import TaskList
from app.domain.utils import verify_token


TASK1 = TaskList(id=1, name="Lista 1")
TASK2 = TaskList(id=2, name="Lista 2")


@pytest.fixture
def mock_usecase():
    return AsyncMock(spec=TaskListUsecase)

@pytest.fixture
def client(mock_usecase, override_auth_dependency):
    app = FastAPI()
    router = create_task_lists_route(mock_usecase)
    app.include_router(router, prefix="/api/v1")
    app.dependency_overrides[verify_token] = override_auth_dependency
    return TestClient(app)

def test_get_task_lists(client, mock_usecase):
    mock_usecase.get_lists.return_value = [
        TASK1,
        TASK2,
    ]
    
    response = client.get("/api/v1/task-lists")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert "completion_percentage" in data[0]
    assert data[0]["id"] == 1
    assert data[0]["name"] == "Lista 1"
    
def test_get_task_list(client, mock_usecase):
    mock_usecase.get_list_by_id.return_value = TASK1
    
    response = client.get("/api/v1/task-lists/1")
    
    assert response.status_code == 200
    data = response.json()
    assert "completion_percentage" in data
    
def test_not_exist_list(client, mock_usecase):
    mock_usecase.get_list_by_id.return_value = None
    
    response = client.get("/api/v1/task-lists/99")
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Task List Not Found"
    
def test_create_list(client, mock_usecase):
    mock_usecase.create_list.return_value = TASK1
    
    payload = {
        "name": "Lista 1"
    }
    
    response = client.post("/api/v1/task-lists", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Task List Created"
    assert "completion_percentage" in data["data"]
    
def test_create_error(client, mock_usecase):
    mock_usecase.create_list.side_effect = ValueError("Some Error")
    
    payload = {
        "name": "Lista"
    }
    
    response = client.post("/api/v1/task-lists", json=payload)
    
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Some Error"
    
def test_update_list(client, mock_usecase):
    mock_usecase.update_list.return_value = TASK2
    
    payload = {
        "name": "Lista 2"
    }
    
    response = client.put("/api/v1/task-lists/2", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Task List Updated"

def test_update_exception(client, mock_usecase):
    mock_usecase.update_list.side_effect = ValueError("Some Error")
    
    payload = {
        "name": "Lista 2"
    }
    
    response = client.put("/api/v1/task-lists/2", json=payload)
    
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Some Error"
    
def test_delete_list(client, mock_usecase):
    mock_usecase.delete_list.return_value = True
    
    response = client.delete("/api/v1/task-lists/1")
    
    assert response.status_code == 204

def test_delete_false(client, mock_usecase):
    mock_usecase.delete_list.return_value = False
    
    response = client.delete("/api/v1/task-lists/99")
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Task List Could Not Be Deleted"
    
def test_delete_exception(client, mock_usecase):
    mock_usecase.delete_list.side_effect = ValueError("Some Error")
    
    response = client.delete("/api/v1/task-lists/99")
    
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Some Error"
