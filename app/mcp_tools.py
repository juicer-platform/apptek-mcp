from fastapi import APIRouter
import asyncio

# Example MCP tool: health_check
async def health_check() -> dict:
    """Check MCP server health. Returns status and message."""
    return {"status": "ok", "message": "Apptek MCP server is running"}

tools = {
    "health_check": health_check,
    # Add more tools here as needed
}

mcp_router = APIRouter()

@mcp_router.post("/mcp/execute")
async def execute_tool(request: dict):
    tool_name = request.get("tool_name")
    params = request.get("params", {})
    tool = tools.get(tool_name)
    if not tool:
        return {"error": f"Tool '{tool_name}' not found"}
    if asyncio.iscoroutinefunction(tool):
        return await tool(**params)
    elif callable(tool):
        return tool(**params)
    return {"error": f"Tool '{tool_name}' is not callable"}

@mcp_router.get("/mcp/list")
async def list_tools():
    return [{"name": name, "description": func.__doc__ or ""} for name, func in tools.items()]
