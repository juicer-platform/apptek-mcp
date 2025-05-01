# Apptek MCP Server

This project implements a Model Context Protocol (MCP) server for Apptek ASR, TTS, and MT APIs using FastAPI and FastMCP.

## Structure
- `app/`: main application code
- `tests/`: test suite
- `scripts/`: utility scripts

## Setup
- Python 3.8+
- Dependency management: [uv](https://github.com/astral-sh/uv)
- Set up your environment variables in a `.env` file:
  ```env
  APPTEK_API_TOKEN=your-apptek-api-token
  ```

## Quickstart
```sh
uv venv .venv
uv pip install fastapi fastmcp uvicorn pytest httpx pydantic-settings
```

## API Authentication
- All endpoints (except `/` and `/health/`) require an API token via the `x-token` HTTP header.
- Example:
  ```http
  x-token: your-apptek-api-token
  ```

## Endpoints
- `GET /health/`: Health check (no auth required)
- `GET /health/services`: Lists available Apptek services using the v2 API (`https://api.apptek.com/api/v2/services`). Requires `x-token` header.

## Development
- Run the API: `uvicorn app.main:app --reload`
- Run tests: `.venv/bin/python -m pytest -v`
