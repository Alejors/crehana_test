from fastapi import FastAPI

from app.infrastructure import Base, engine

# Models
from app.domain import models # noqa: F401

# Usecases
from app.usecases import Healthcheck

# Controllers/Routers
from app.api.v1 import create_healthcheck_route


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Tasks Manager App")

healthcheck_usecase = Healthcheck()

healthcheck_router = create_healthcheck_route(healthcheck_usecase)

v1_routers = [
    healthcheck_router,
]

for router in v1_routers:
    app.include_router(router, prefix="/api/v1")
