from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from app.config import settings
from app.mcp_tools import mcp_router

app = FastAPI(title="Apptek MCP Server", version="0.1.0")

import logging

# Set up logging
logger = logging.getLogger("auth")
logger.setLevel(logging.INFO)

# Authentication utility

def extract_token(request: Request):
    # Apptek API requires x-token header
    return request.headers.get("x-token")

@app.middleware("http")
async def authenticate_request(request: Request, call_next):
    # Allow health and root endpoints without auth
    if request.url.path in ["/", "/health", "/health/"]:
        return await call_next(request)
    token = extract_token(request)
    print("token sent from request:", token)
    if not token:
        logger.warning(f"Auth failed: missing token from {request.client.host} {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Missing API token. Provide in x-token header."}
        )
    # No server-side token check; any token is accepted

    logger.info(f"Auth success: {request.client.host} {request.url.path}")
    return await call_next(request)

@app.get("/")
def root():
    return {"message": "Welcome to the Apptek MCP Server"}

# Routers for ASR, TTS, MT, health, and language identification will be added here
# Example router structure for future endpoints
asr_router = APIRouter(prefix="/asr", tags=["ASR"])
tts_router = APIRouter(prefix="/tts", tags=["TTS"])
mt_router = APIRouter(prefix="/mt", tags=["MT"])
health_router = APIRouter(prefix="/health", tags=["Health"])

@health_router.get("/", summary="Health check")
async def health_check():
    return {"status": "ok", "message": "Apptek MCP server is running"}

@health_router.get("/services", summary="List available Apptek services")
async def get_services():
    url = "https://api.apptek.com/api/v2/services"
    headers = {"x-token": settings.APPTEK_API_TOKEN}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Apptek API error: {e.response.status_code} {e.response.text}")
        return JSONResponse(status_code=e.response.status_code, content={"detail": "Apptek API error", "error": e.response.text})
    except Exception as e:
        logger.error(f"Apptek API connection error: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": "Failed to connect to Apptek API", "error": str(e)})
lid_router = APIRouter(prefix="/lid", tags=["Language ID"])

# Register routers (endpoints to be implemented)
app.include_router(asr_router)
app.include_router(tts_router)
app.include_router(mt_router)
app.include_router(health_router)
app.include_router(lid_router)
app.include_router(mcp_router)
