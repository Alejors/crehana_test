import pytest
from fastapi import FastAPI
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from app.domain.entities import User
from app.usecases import UserUsecase
from app.api.v1 import create_user_route


USER = User(
    email="test@test.com",
    password="$2b$12$F1DlWKoiKLMMnjT/n0Q56eedZK/lmUvxGk3EO5QYI55VXYuNYTZ2y",
    username="Test-1",
    id=1,
)

TOKEN = "token123456"


@pytest.fixture
def mock_usecase():
    return AsyncMock(spec=UserUsecase)


@pytest.fixture
def client(mock_usecase):
    app = FastAPI()
    router = create_user_route(mock_usecase)
    app.include_router(router, prefix="/api/v1")
    return TestClient(app)


def test_register(client, mock_usecase):
    mock_usecase.create_user.return_value = USER

    payload = {"email": "test@test.com", "password": "Random1234", "username": "Test-1"}

    response = client.post("/api/v1/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert data["message"] == "Registration Successful"
    assert "data" in data
    assert data["data"]["username"] == "Test-1"


def test_register_exception(client, mock_usecase):
    mock_usecase.create_user.side_effect = ValueError("Some Error")

    payload = {"email": "test@test.com", "password": "Random1234", "username": "Test-1"}

    response = client.post("/api/v1/register", json=payload)

    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Some Error"


def test_login(client, mock_usecase):
    mock_usecase.login_user.return_value = (USER, TOKEN)

    payload = {
        "email": "test@test.com",
        "password": "Random1234",
    }

    response = client.post("/api/v1/login", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.cookies


def test_failed_login(client, mock_usecase):
    mock_usecase.login_user.return_value = (None, None)

    payload = {
        "email": "test@test.com",
        "password": "Random1234",
    }

    response = client.post("/api/v1/login", json=payload)

    assert response.status_code == 404
    assert "access_token" not in response.cookies
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Email and/or Password Incorrect"


def test_login_exception(client, mock_usecase):
    mock_usecase.login_user.side_effect = ValueError("Some Error")

    payload = {
        "email": "test@test.com",
        "password": "Random1234",
    }

    response = client.post("/api/v1/login", json=payload)

    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "Some Error"


def test_logout(client):
    # Seteamos la cookie manualmente en el cliente
    client.cookies.set("access_token", TOKEN)

    # Al pegarle al endpoint de logout se elimina
    response = client.post("/api/v1/logout")

    assert response.status_code == 204
    # Validamos que la cookie se eliminó
    assert "access_token" not in response.cookies
