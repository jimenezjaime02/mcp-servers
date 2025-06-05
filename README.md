# MCP Servers Project

This repository demonstrates a few small MCP servers built with the `mcp` Python SDK. Each script exposes its own tool that can run in stdio mode or via an optional HTTP endpoint.

## Server overview

- **`app.py`** – A minimal Flask application exposing a single `/health` endpoint used by the health check server.
- **`coding_practices_server.py`** – Provides the `get_best_practices` tool returning recommended Python coding practices.
- **`health_check_server.py`** – Runs system health checks through the `run_health_checks` tool. It can ping a configurable health URL and optionally check a database and other services.
- **`mcp_practices_server.py`** – Offers `get_mcp_server_best_practices` with tips for writing MCP servers.

## Requirements

- Python 3.8+
- Packages: `mcp[cli]`, `flask`, `requests`, `psycopg2-binary` (required only for database checks)

Install dependencies with:

```bash
pip install mcp[cli] flask requests psycopg2-binary
```

## Usage

Start the Flask app:

```bash
python app.py
```

Run the servers individually (stdio mode by default):

```bash
python coding_practices_server.py
python health_check_server.py
python mcp_practices_server.py
```

Add `--transport streamable-http --port <port>` to any server command to run it over HTTP.

### Health check configuration

`health_check_server.py` supports several environment variables:

- `HEALTH_URL` – URL to ping for the core health check (default `http://localhost:5000/health`).
- `DATABASE_URL` – PostgreSQL connection string used to verify database connectivity.
- `EXTRA_HEALTH_URLS` – Comma-separated additional URLs for service health checks.

## Contributing

Feel free to open issues or submit pull requests.

## License

Add your license here (e.g., MIT License)
