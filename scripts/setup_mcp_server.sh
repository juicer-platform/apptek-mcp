#!/bin/bash
# Automated setup for Apptek MCP FastMCP server
set -e

# 1. Create and activate virtual environment if not exists
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

# 2. Install dependencies
pip install --upgrade pip
pip install fastmcp python-dotenv

# 3. Prompt for API key if not present in .env
if [ ! -f .env ] || ! grep -q "APPTEK_API_TOKEN=" .env; then
  echo "Enter your APPTEK_API_TOKEN (will be saved to .env):"
  read -r TOKEN
  echo "APPTEK_API_TOKEN=$TOKEN" > .env
else
  echo ".env with APPTEK_API_TOKEN already exists."
fi

# 4. Register the MCP server script with fastmcp
.venv/bin/fastmcp install mcp_server.py

echo "\nSetup complete!"
echo "To run your MCP server:"
echo "  source .venv/bin/activate && python mcp_server.py"
echo "Or:"
echo "  .venv/bin/fastmcp run mcp_server.py"
