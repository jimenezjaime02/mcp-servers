'''MCP server providing best practices for implementing MCP servers in Python for Windsurf.

Usage (CLI):

    python mcp_practices_server.py

Example (HTTP):

    python mcp_practices_server.py --transport streamable-http --port 8000
'''

from typing import List

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP('MCPServerPractices')

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool(description='Return best-practice tips for implementing MCP servers in Python for Windsurf.')
def get_mcp_server_best_practices() -> List[str]:
    return [
        'Use the official Python SDK: install with `pip install \'mcp[cli]\'` and leverage FastMCP for setup',
        'Define tools and resources with decorators: use `@mcp.tool()` and `@mcp.resource()` for clear API exposure',
        'Structure code into modules: separate server setup, tool implementation, and configuration for maintainability',
        'Implement robust error handling and logging: use Python logging module to capture server activities and errors',
        'Secure your server: add authentication/authorization (e.g., OAuth) and avoid hardcoding sensitive information',
        'Test locally with MCP Inspector: run `mcp dev mcp_practices_server.py` to validate functionality before integration',
        'Configure for Windsurf integration: ensure server startup command is specified in mcp_config.json',
        'Follow the MCP specification: adhere to endpoints and transports (stdio, SSE, HTTP) for compatibility',
        'Use virtual environments: isolate dependencies with venv or conda to maintain consistent environments',
        'Document and version control: provide clear README, docstrings, and use version control for changes',
    ]

if __name__ == '__main__':
    mcp.run()
