from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Daily Hidayah API. Visit /guidance for inspiration."}

def test_get_guidance():
    response = client.get("/guidance")
    assert response.status_code == 200
    data = response.json()
    assert "type" in data
    assert "content" in data
    assert "source" in data
    assert data["type"] in ["ayah", "hadith"]

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"http_requests_total" in response.content
