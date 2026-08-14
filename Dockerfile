# =============================================================================
# Stage 1: Build — install dependencies into an isolated venv
# =============================================================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system build tools only if required by wheel builds.
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Build a small isolated virtual environment for runtime dependencies.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt pyproject.toml ./
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy source after dependency install to maximize cache efficiency.
COPY . .

# =============================================================================
# Stage 2: Runner — minimal production image
# =============================================================================
FROM python:3.12-slim AS runner

LABEL org.opencontainers.image.title="Multi-Agent Framework API"
LABEL org.opencontainers.image.description="FastAPI backend for the Multi-Agent Orchestration Framework"
LABEL org.opencontainers.image.source="https://github.com/your-org/multi-agent-framework-api"

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/sh --create-home appuser

WORKDIR /app
COPY --from=builder /app /app
RUN chown -R appuser:appgroup /app

COPY --from=builder /app/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

RUN mkdir -p /data/uploads && chown -R appuser:appgroup /data
VOLUME ["/data"]

USER appuser

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health', timeout=5)" >/dev/null 2>&1 || exit 1

ENTRYPOINT ["/docker-entrypoint.sh"]
