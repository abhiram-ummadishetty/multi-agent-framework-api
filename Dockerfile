# =============================================================================
# Stage 1: Build — install dependencies into an isolated venv
# =============================================================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system build tools needed by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment inside the image for clean layer separation
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies first (cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =============================================================================
# Stage 2: Runner — minimal production image
# =============================================================================
FROM python:3.12-slim AS runner

LABEL org.opencontainers.image.title="Multi-Agent Framework API"
LABEL org.opencontainers.image.description="FastAPI backend for the Multi-Agent Orchestration Framework"
LABEL org.opencontainers.image.source="https://github.com/your-org/multi-agent-framework-api"

# Runtime system deps only (libpq for postgres driver if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the pre-built venv from builder (no compiler toolchain in production image)
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# ── Non-root user ─────────────────────────────────────────────────────────────
# Running as root in a container is a security anti-pattern.
RUN groupadd --gid 1001 appgroup && \
    useradd  --uid 1001 --gid appgroup --shell /bin/sh --create-home appuser

WORKDIR /app

# Copy application source
COPY --chown=appuser:appgroup . .

# Copy and enable entrypoint
COPY --chown=appuser:appgroup docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# ── Data volume ───────────────────────────────────────────────────────────────
# Persistent storage for uploads (and SQLite in dev). Mount a real volume in
# production to survive container restarts.
RUN mkdir -p /data/uploads && chown -R appuser:appgroup /data
VOLUME ["/data"]

USER appuser

EXPOSE 8001

# ── Health check ──────────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

ENTRYPOINT ["/docker-entrypoint.sh"]
