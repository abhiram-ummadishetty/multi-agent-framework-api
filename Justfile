# Justfile - developer recipes

set shell := ["bash", "-lc"]

default: help

help:
    @echo "Available recipes: setup, install, run, test, lint, format, clean"

setup:
    @echo "Creating virtualenv and installing uv..."
    python -m venv .venv
    source .venv/bin/activate && python -m pip install --upgrade pip
    source .venv/bin/activate && pip install uv
    source .venv/bin/activate && uv install || echo "Run 'uv install' to install from pyproject.toml"

install:
    @echo "Install dependencies into active venv (or create with just setup)"
    source .venv/bin/activate && pip install -r requirements.txt || echo "Use 'just setup' to create venv and install uv"

run:
    @echo "Run the FastAPI app locally"
    source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000

test:
    @echo "Run tests"
    source .venv/bin/activate && pytest -q

lint:
    @echo "Lint with ruff if available"
    source .venv/bin/activate && (ruff check . || echo "Install ruff in the venv to run linting: pip install ruff")

format:
    @echo "Format with ruff if available"
    source .venv/bin/activate && (ruff format . || echo "Install ruff in the venv to run formatting: pip install ruff")

clean:
    @echo "Remove venv and caches"
    rm -rf .venv .pytest_cache __pycache__ .ruff_cache
