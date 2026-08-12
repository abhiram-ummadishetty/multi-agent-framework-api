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
just setup    # create venv, install uv, and install deps
just run      # run the API locally on http://localhost:8000
just test     # run tests
just clean    # remove venv and caches
```


