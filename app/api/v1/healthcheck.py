from fastapi import APIRouter
from app.usecases import Healthcheck


def create_healthcheck_route(healthcheck_usecase: Healthcheck) -> APIRouter:

    router: APIRouter = APIRouter()

    @router.get("/ping")
    async def ping():
        return await healthcheck_usecase.ping()

    return router
