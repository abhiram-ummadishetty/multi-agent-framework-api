#!/bin/sh
# docker-entrypoint.sh
#
# Runs before uvicorn starts inside the container.
# Responsibilities:
#   1. Ensure required data directories exist with correct ownership
#   2. Print a startup summary (no secret values are logged)
#   3. Exec uvicorn — PID 1 for proper signal handling

set -e

# ── Data directories ──────────────────────────────────────────────────────────
UPLOAD_DIR="${UPLOAD_DIR:-/data/uploads}"
DATA_DIR="${UPLOAD_DIR%/*}"   # parent dir (e.g. /data)

mkdir -p "$UPLOAD_DIR"
# Ensure the running user owns the dir (relevant when mounted volumes are root-owned)
chown -R "$(id -u):$(id -g)" "$DATA_DIR" 2>/dev/null || true

# ── Startup summary ───────────────────────────────────────────────────────────
echo "========================================"
echo " Multi-Agent Framework API"
echo "========================================"
echo " Environment : ${APP_ENV:-development}"
echo " LLM provider: ${LLM_PROVIDER:-stub}"
echo " Vector store: ${VECTOR_STORE_TYPE:-memory}"
echo " Upload dir  : ${UPLOAD_DIR}"
echo " Log level   : ${LOG_LEVEL:-info}"
echo " Port        : ${API_PORT:-8001}"
echo "========================================"

# ── Exec uvicorn (replaces shell, PID 1) ─────────────────────────────────────
exec uvicorn main:app \
    --host "${API_HOST:-0.0.0.0}" \
    --port "${API_PORT:-8001}" \
    --log-level "${LOG_LEVEL:-info}" \
    --no-access-log
