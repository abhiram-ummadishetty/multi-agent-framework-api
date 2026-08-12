"""
Multi-Agent Framework API — Main Entry Point
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from routers import chat, upload, history, feedback, agents

settings = get_settings()

# Configure basic logging
logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
logger = logging.getLogger("multi-agent-framework-api")

# Initialize Sentry if configured
if settings.sentry_dsn:
    try:
        import sentry_sdk

        sentry_sdk.init(dsn=settings.sentry_dsn)
        logger.info("Sentry initialized")
    except Exception:
        logger.exception("Failed to initialize Sentry")

app = FastAPI(
    title="Multi-Agent Framework API",
    description="Gateway API for the Local LLM Multi-Agent Orchestration Framework",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router,     prefix="/chat",     tags=["Chat"])
app.include_router(upload.router,   prefix="/upload",   tags=["Upload"])
app.include_router(history.router,  prefix="/history",  tags=["History"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
app.include_router(agents.router,   prefix="/agents",   tags=["Agents"])


@app.on_event("startup")
async def on_startup():
    logger.info("Starting multi-agent-framework-api (env=%s)", settings.app_env)


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down multi-agent-framework-api")


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "service": "multi-agent-framework-api"}


@app.get("/settings", tags=["Health"], include_in_schema=not settings.is_production)
async def show_settings():
    """
    Returns active (non-secret) settings for debugging.
    Disabled in production — secrets are never exposed.
    """
    if settings.is_production:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "app_env":             settings.app_env,
        "llm_provider":        settings.llm_provider,
        "ollama_model":        settings.ollama_model,
        "openai_model":        settings.openai_model,
        "anthropic_model":     settings.anthropic_model,
        "gemini_model":        settings.gemini_model,
        "embedding_provider":  settings.embedding_provider,
        "vector_store_type":   settings.vector_store_type,
        "chroma_host":         settings.chroma_host,
        "database_url":        settings.database_url.split("@")[-1] if "@" in settings.database_url else settings.database_url,
        "upload_dir":          settings.upload_dir,
        "max_upload_size_mb":  settings.max_upload_size_mb,
        "allowed_origins":     settings.allowed_origins,
        "log_level":           settings.log_level,
        "agent_timeout_seconds": settings.agent_timeout_seconds,
        "max_concurrent_agents": settings.max_concurrent_agents,
        # Keys shown as present/absent — values never logged
        "openai_api_key_set":     bool(settings.openai_api_key),
        "anthropic_api_key_set":  bool(settings.anthropic_api_key),
        "gemini_api_key_set":     bool(settings.gemini_api_key),
        "pinecone_api_key_set":   bool(settings.pinecone_api_key),
        "weaviate_api_key_set":   bool(settings.weaviate_api_key),
        "sentry_dsn_set":         bool(settings.sentry_dsn),
    }
