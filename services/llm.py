"""
Stub LLM service — simulates local LLM responses.
Replace with actual LLM client (Ollama, GCP, OpenAI) later.
"""
import asyncio
import random
from typing import AsyncGenerator

STUB_RESPONSES = [
    "I'm the Multi-Agent Orchestrator. I've received your query and I'm routing it to the most suitable agent in the framework.",
    "Based on your request, I'm engaging the RAG Agent to search through the vector store for relevant context. This ensures my response is grounded in your enterprise data.",
    "I've analyzed your prompt and identified it as a data analysis task. Dispatching to AI Agent 2 which specializes in data processing and analytics.",
    "The MCP Server has retrieved the relevant tools needed to fulfill your request. Processing your query through the agent pipeline now.",
    "Your query has been processed through the multi-agent framework. The Orchestrator coordinated between AI Agent 1 and the RAG Agent to synthesize this comprehensive response.",
    "I'm connected to the local LLM inference engine (gpt-oss-120B on GCP GKE). Generating a response tailored to your enterprise context...",
]


async def stub_llm_response(prompt: str) -> str:
    """Simulate a non-streaming LLM response with a small delay."""
    await asyncio.sleep(0.8)
    base = random.choice(STUB_RESPONSES)
    return f"{base}\n\n> **Your query:** {prompt}"


async def stub_stream_response(prompt: str) -> AsyncGenerator[str, None]:
    """Simulate a token-by-token streaming response."""
    base = random.choice(STUB_RESPONSES)
    full = f"{base}\n\n> **Your query:** {prompt}"

    # Split into word-level tokens to simulate streaming
    words = full.split(" ")
    for i, word in enumerate(words):
        token = word + (" " if i < len(words) - 1 else "")
        yield token
        await asyncio.sleep(random.uniform(0.03, 0.08))  # simulate LLM token speed
