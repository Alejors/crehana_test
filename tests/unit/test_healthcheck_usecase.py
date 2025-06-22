import pytest
from app.usecases import Healthcheck


@pytest.mark.asyncio
async def test_healthcheck_ping():
    usecase = Healthcheck()
    response = await usecase.ping()
    assert response["message"] == "pong"
