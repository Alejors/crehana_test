from fastapi import FastAPI
from app.api.v1 import router as api_router

app = FastAPI(title="Todo App")

app.include_router(api_router, prefix="/api/v1")
