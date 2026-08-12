"""
LLM service layer — delegates to a configured external LLM client when available,
otherwise falls back to a lightweight stub implementation for local development.
"""
import asyncio
import random
from typing import AsyncGenerator
from config import get_settings

# Optional external LLM client
try:
    from clients.external_llm import generate as external_generate, stream as external_stream
except Exception:
    external_generate = None
    external_stream = None

STUB_RESPONSES = [
    "I'm the Multi-Agent Orchestrator. I've received your query and I'm routing it to the most suitable agent in the framework.",
    "Based on your request, I'm engaging the RAG Agent to search through the vector store for relevant context. This ensures my response is grounded in your enterprise data.",
    "I've analyzed your prompt and identified it as a data analysis task. Dispatching to AI Agent 2 which specializes in data processing and analytics.",
    "The MCP Server has retrieved the relevant tools needed to fulfill your request. Processing your query through the agent pipeline now.",
    "Your query has been processed through the multi-agent framework. The Orchestrator coordinated between AI Agent 1 and the RAG Agent to synthesize this comprehensive response.",
    "I'm connected to the local LLM inference engine (gpt-oss-120B on GCP GKE). Generating a response tailored to your enterprise context...",
]

settings = get_settings()


async def stub_llm_response(prompt: str) -> str:
    """Return a full response. If an external LLM URL is configured, use it."""
    if settings.external_llm_url and external_generate:
        return await external_generate(prompt)

    # local stub
    await asyncio.sleep(0.8)
    base = random.choice(STUB_RESPONSES)
    return f"{base}\n\n> **Your query:** {prompt}"


async def stub_stream_response(prompt: str) -> AsyncGenerator[str, None]:
    """Stream tokens. If external LLM streaming is available, stream from it."""
    if settings.external_llm_url and external_stream:
        async for token in external_stream(prompt):
            yield token
        return

    # local stub streaming
    base = random.choice(STUB_RESPONSES)
    full = f"{base}\n\n> **Your query:** {prompt}"

    # Split into word-level tokens to simulate streaming
    words = full.split(" ")
    for i, word in enumerate(words):
        token = word + (" " if i < len(words) - 1 else "")
        yield token
        await asyncio.sleep(random.uniform(0.03, 0.08))  # simulate LLM token speed
