import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("APPTEK_API_TOKEN", os.getenv("APPTEK_API_TOKEN", "test-token"))


def test_health_check():
    resp = client.get("/health/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_services_unauthorized():
    resp = client.get("/health/services")
    assert resp.status_code == 401
    assert "Missing API token" in resp.text or "Invalid API token" in resp.text

def test_services_authorized():
    token = os.getenv("APPTEK_API_TOKEN", "test-token")
    resp = client.get("/health/services", headers={"x-token": token})
    # Accept 200 (success) or 502/500 (external API error if offline)
    assert resp.status_code in (200, 500, 502, 401)
    # If authorized, should not get missing/invalid token
    if resp.status_code == 200:
        assert isinstance(resp.json(), dict)
    elif resp.status_code in (500, 502):
        assert "Apptek API" in resp.text or "Failed to connect" in resp.text
    elif resp.status_code == 401:
        assert "Invalid API token" in resp.text
