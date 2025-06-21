from fastapi import FastAPI
from app.api.v1 import router as api_router
from app.infrastructure import Base, engine
from app.domain import models


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Tasks Manager App")

app.include_router(api_router, prefix="/api/v1")
