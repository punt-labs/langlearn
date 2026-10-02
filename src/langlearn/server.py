from __future__ import annotations

from fastmcp import FastMCP

from langlearn import __version__

mcp = FastMCP("langlearn", version=__version__)


@mcp.tool()
def ping() -> str:
    "Health check tool."
    return "ok"


def run_server() -> None:
    "Run the MCP server."
    mcp.run()
