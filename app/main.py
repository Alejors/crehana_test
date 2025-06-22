from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.infrastructure.db import init_models, SessionLocal

# Repositories
from app.infrastructure.repositories import (
    SQLAlchemyTaskListRepository,
    SQLAlchemyTaskRepository,
    SQLAlchemyUserRepository,
)

# Services
from app.infrastructure.services import TerminalMailingService

# Usecases
from app.usecases import (
    Healthcheck,
    TaskListUsecase,
    TaskUsecase,
    UserUsecase,
)

# Controllers/Routers
from app.api.v1 import (
    create_healthcheck_route,
    create_task_lists_route,
    create_task_route,
    create_user_route,
)

# Custom Exceptions
from app.exceptions import TaskListDeletionError


app = FastAPI(title="Tasks Manager App")


@app.exception_handler(TaskListDeletionError)
async def task_list_deletion_exception_handler(
    request: Request, exc: TaskListDeletionError
):
    return JSONResponse(status_code=400, content={"detail": exc.message})


# Repositories
sqlalchemy_task_list_repository = SQLAlchemyTaskListRepository(SessionLocal)
sqlalchemy_task_repository = SQLAlchemyTaskRepository(SessionLocal)
sqlalchemy_user_repository = SQLAlchemyUserRepository(SessionLocal)

# Services
terminal_mailing_service = TerminalMailingService()

# Usecases
healthcheck_usecase = Healthcheck()
task_list_usecase = TaskListUsecase(sqlalchemy_task_list_repository)
task_usecase = TaskUsecase(
    sqlalchemy_task_repository,
    sqlalchemy_task_list_repository,
    sqlalchemy_user_repository,
    terminal_mailing_service,
)
user_usecase = UserUsecase(sqlalchemy_user_repository)

healthcheck_router = create_healthcheck_route(healthcheck_usecase)
task_list_router = create_task_lists_route(task_list_usecase)
task_router = create_task_route(task_usecase)
user_router = create_user_route(user_usecase)

v1_routers = [
    healthcheck_router,
    task_list_router,
    task_router,
    user_router,
]

for router in v1_routers:
    app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    await init_models()
