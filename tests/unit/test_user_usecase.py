import pytest
from unittest.mock import AsyncMock

from app.domain.entities import User
from app.usecases import UserUsecase


USER = User(
    "test@test.com",
    "$2b$12$F1DlWKoiKLMMnjT/n0Q56eedZK/lmUvxGk3EO5QYI55VXYuNYTZ2y",
    id=1,
)


@pytest.mark.asyncio
async def test_create_user(mock_user_repo):
    mock_user_repo.create_user = AsyncMock(return_value=USER)

    usecase = UserUsecase(mock_user_repo)

    user_in = User("test@test.com", "random1234")

    result = await usecase.create_user(user_in)

    assert isinstance(result, User)
    assert result.id == 1


@pytest.mark.asyncio
async def test_login(mock_user_repo):
    mock_user_repo.get_user_by_email = AsyncMock(return_value=USER)

    usecase = UserUsecase(mock_user_repo)

    user_in = User("test@test.com", "random1234")

    result, token = await usecase.login_user(user_in)

    assert isinstance(result, User)
    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_login_user_not_exist(mock_user_repo):
    mock_user_repo.get_user_by_email = AsyncMock(return_value=None)

    usecase = UserUsecase(mock_user_repo)

    user_in = User("test@test.com", "random1234")

    result, token = await usecase.login_user(user_in)

    assert result is None
    assert token is None


@pytest.mark.asyncio
async def test_login_wrong_password(mock_user_repo):
    mock_user_repo.get_user_by_email = AsyncMock(return_value=USER)

    usecase = UserUsecase(mock_user_repo)

    user_in = User("test@test.com", "wrong1234")

    result, token = await usecase.login_user(user_in)

    assert result is None
    assert token is None
