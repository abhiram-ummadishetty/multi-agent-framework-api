# multi-agent-framework-api

This repository provides a FastAPI-based multi-agent framework API.

Quick start (using `uv` package manager):

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install `uv` (if you want to use it) and install dependencies from `pyproject.toml`:

```bash
pip install --upgrade pip
pip install uv
uv install
```

If you prefer the classic workflow, install from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Developer recipes are provided in the `Justfile`.

Examples:

```bash
just setup      # create venv, install uv, and install deps
just install    # install dependencies from requirements.txt
just uvinstall  # install dependencies from pyproject.toml using uv
just run        # run the API locally on http://localhost:8000
uv run uvicorn bootstrap:app --reload --host 0.0.0.0 --port 8000
just test       # run tests
just clean      # remove venv and caches
```

The production bootstrap entrypoint is:

```bash
uvicorn bootstrap:app --reload --host 0.0.0.0 --port 8000
```

API routes are versioned under `/v1`, for example:

- `POST /v1/chat`
- `POST /v1/upload`
- `GET /v1/history`
- `GET /health`

## Database & Cloud SQL Proxy

The app uses SQLAlchemy async persistence. By default it runs with SQLite via `sqlite+aiosqlite:///./data/app.db`.

For PostgreSQL / Cloud SQL proxy:

```bash
DATABASE_URL=postgresql+psycopg://user:password@127.0.0.1:5432/agentdb
```

Then run the Cloud SQL proxy locally and point the app at `127.0.0.1:5432`. Example:

```bash
./cloud_sql_proxy --instances=PROJECT:REGION:INSTANCE=tcp:5432
```

Keep secrets out of source control and only store credentials in `.env` or Kubernetes secrets.



