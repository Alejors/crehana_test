import pytest
from unittest.mock import AsyncMock
from app.domain.interfaces import (
    ITaskListRepository,
    ITaskRepository,
    IUserRepository,
    IMailingService,
)


@pytest.fixture
def mock_task_list_repo():
    repo = AsyncMock(spec=ITaskListRepository)
    return repo


@pytest.fixture
def mock_task_repo():
    repo = AsyncMock(spec=ITaskRepository)
    return repo


@pytest.fixture
def mock_user_repo():
    repo = AsyncMock(spec=IUserRepository)
    return repo


@pytest.fixture
def mock_mailing_service():
    service = AsyncMock(spec=IMailingService)
    return service


@pytest.fixture
def override_auth_dependency():
    def fake_auth():
        return True

    return fake_auth
