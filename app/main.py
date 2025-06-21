from fastapi import FastAPI

from app.infrastructure.db import init_models, SessionLocal

# Repositories
from app.infrastructure.repositories import SQLAlchemyTaskListRepository

# Usecases
from app.usecases import Healthcheck, TaskListUsecase

# Controllers/Routers
from app.api.v1 import create_healthcheck_route, create_task_lists_route


app = FastAPI(title="Tasks Manager App")

sqlalchemy_task_list_repository = SQLAlchemyTaskListRepository(SessionLocal)

healthcheck_usecase = Healthcheck()
task_list_usecase = TaskListUsecase(sqlalchemy_task_list_repository)

healthcheck_router = create_healthcheck_route(healthcheck_usecase)
task_list_router = create_task_lists_route(task_list_usecase)

v1_routers = [
    healthcheck_router,
    task_list_router,
]

for router in v1_routers:
    app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def on_startup():
    await init_models()
