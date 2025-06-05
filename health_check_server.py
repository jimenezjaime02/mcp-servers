"""
MCP server providing health checks for your system.

This server exposes a single tool `run_health_checks` that:
  1. Pings an HTTP health endpoint.
  2. Optionally verifies a database connection if `DATABASE_URL` is set.
  3. Optionally checks additional service health endpoints via `EXTRA_HEALTH_URLS`.

Usage (stdio):
    python health_check_server.py

Usage (HTTP mode):
    python health_check_server.py --transport streamable-http --port 5001
"""

from typing import Dict
from mcp.server.fastmcp import FastMCP
import requests
import os

# Initialize the FastMCP server
mcp = FastMCP("HealthCheck")

@mcp.tool(description="Run core health checks for the system and optional additional service health checks via EXTRA_HEALTH_URLS")
def run_health_checks() -> Dict[str, str]:
    status = "ok"
    details = []

    # 1) HTTP health endpoint check
    endpoint = os.environ.get("HEALTH_URL", "http://localhost:5000/health")
    try:
        resp = requests.get(endpoint, timeout=5)
        if resp.status_code != 200:
            status = "error"
            details.append(f"Health endpoint {endpoint} returned status code {resp.status_code}")
    except Exception as e:
        status = "error"
        details.append(f"Health endpoint {endpoint} request failed: {e}")

    # 2) Optional DB connectivity check
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        try:
            import psycopg2
            conn = psycopg2.connect(db_url, connect_timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
        except Exception as e:
            status = "error"
            details.append(f"Database ping failed: {e}")

    # 3) Additional service health checks via EXTRA_HEALTH_URLS
    extra_endpoints = os.environ.get("EXTRA_HEALTH_URLS")
    if extra_endpoints:
        for url in extra_endpoints.split(","):
            url = url.strip()
            if not url:
                continue
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code != 200:
                    status = "error"
                    details.append(f"Extra endpoint {url} returned status code {resp.status_code}")
            except Exception as e:
                status = "error"
                details.append(f"Extra endpoint {url} request failed: {e}")

    return {"status": status, "details": "; ".join(details) if details else "All checks passed"}

# Entrypoint
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Health Check MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport type: 'stdio' (default) or 'streamable-http'",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host for HTTP mode")
    parser.add_argument("--port", type=int, default=5001, help="Port for HTTP mode")
    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run()
    else:
        mcp.run(host=args.host, port=args.port, transport="streamable-http")
