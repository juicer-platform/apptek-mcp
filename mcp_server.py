import os
from fastmcp import FastMCP, Context
from dotenv import load_dotenv

# Load .env file
load_dotenv()
API_KEY = os.getenv("APPTEK_API_TOKEN")

mcp = FastMCP("Apptek MCP Context Server")

@mcp.tool()
async def health_check(ctx: Context) -> dict:
    """Check MCP server health. Requires valid API key in x-token header."""
    api_key = ctx.headers.get("x-token")
    if not api_key or api_key != API_KEY:
        return {"status": "error", "message": "Invalid or missing API key"}
    return {"status": "ok", "message": "Apptek MCP server is running"}

if __name__ == "__main__":
    mcp.run()
