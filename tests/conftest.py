import pytest
from unittest.mock import AsyncMock
from app.domain.interfaces import ITaskListRepository


@pytest.fixture
def mock_task_list_repo():
    repo = AsyncMock(spec=ITaskListRepository)
    return repo
