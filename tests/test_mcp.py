import os
os.environ["APPTEK_API_TOKEN"] = os.getenv("APPTEK_API_TOKEN", "test-token")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
TOKEN = os.environ["APPTEK_API_TOKEN"]

def test_mcp_health_check_tool():
    resp = client.post(
        "/mcp/execute",
        json={"tool_name": "health_check", "params": {}},
        headers={"x-token": TOKEN}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "Apptek MCP server is running" in data["message"]

def test_mcp_tool_not_found():
    resp = client.post(
        "/mcp/execute",
        json={"tool_name": "not_a_tool", "params": {}},
        headers={"x-token": TOKEN}
    )
    assert resp.status_code == 200 or resp.status_code == 404
    data = resp.json()
    assert "error" in data
    assert "not found" in data["error"]
