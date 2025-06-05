"""
MCP server providing best coding practices for Python.

This implementation uses the Model Context Protocol (MCP) Python SDK.
It exposes a single tool `get_best_practices` that returns a list of
recommended practices. The server can run in two transport modes:

1. Stdio (default) – suitable for direct integration with IDE clients
   like Cascade. The client launches this script and communicates via
   stdin/stdout.

2. Streamable HTTP – optional, started with --transport streamable-http,
   useful for testing with MCP Inspector or making the server available
   at an /mcp endpoint.

Example (stdio, used by Cascade):

    python coding_practices_server.py

Example (HTTP):

    python coding_practices_server.py --transport streamable-http --port 8000
"""

from typing import List

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("CodingPractices")


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool(description="Return a list of best-practice tips for Python coding practices.")
def get_best_practices() -> List[str]:
    return [
        "Follow PEP 8 style guide: use 4 spaces for indentation, limit lines to 79 characters, and use meaningful variable and function names",
        "Write docstrings: include triple double-quoted docstrings for public functions, classes, and modules following PEP 257",
        "Use type hints: annotate function signatures for improved readability and to enable static type checking with tools like mypy",
        "Write tests: use unittest or pytest for unit testing, aim for high coverage, and consider Test-Driven Development (TDD)",
        "Use virtual environments: isolate project dependencies with venv or conda to prevent conflicts",
        "Leverage Pythonic idioms: use list comprehensions and generators for concise and efficient code",
        "Use logging instead of print: choose appropriate logging levels (DEBUG, INFO, ERROR) and include timestamps",
        "Keep code DRY (Don't Repeat Yourself): avoid duplication by using functions, classes, and modules",
        "Use additional tools: employ Pylint, Flake8, and Black for linting and formatting to enforce standards",
    ]


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Coding Practices MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport type: 'stdio' (default) or 'streamable-http'",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host for HTTP mode")
    parser.add_argument("--port", type=int, default=5000, help="Port for HTTP mode")
    args = parser.parse_args()

    if args.transport == "stdio":
        # stdio mode is ideal for IDE integration (Cascade will launch the process)
        mcp.run()
    else:
        # Streamable HTTP mode – exposes an /mcp endpoint compatible with MCP clients
        mcp.run(host=args.host, port=args.port, transport="streamable-http")
