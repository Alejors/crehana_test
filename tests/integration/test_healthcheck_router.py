from fastapi.testclient import TestClient
from app.api.v1.healthcheck import create_healthcheck_route
from app.usecases import Healthcheck
from fastapi import FastAPI

def test_healthcheck_endpoint():
    healthcheck_usecase = Healthcheck()
    router = create_healthcheck_route(healthcheck_usecase)

    app = FastAPI()
    app.include_router(router, prefix="/api/v1")

    client = TestClient(app)
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    
    data = response.json()
    assert data['message'] == "pong"
