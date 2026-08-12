"""Compatibility shim for tooling that expects main.py.

This forwards to the production bootstrap app factory in `bootstrap.py`
so older FastAPI/uvicorn workflows continue to work.
"""
from bootstrap import app  # noqa: F401
