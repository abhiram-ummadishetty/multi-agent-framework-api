"""
Lightweight external LLM client using httpx.
The client supports two helpers:
- `generate(prompt)` -> str
- `stream(prompt)` -> async generator of token strings

The external LLM API is expected to be a simple HTTP JSON API for non-streaming
responses, and for streaming it should support chunked transfer with newline
separated JSON objects or Server-Sent Events.
"""
from typing import AsyncGenerator
import json
import httpx
from config import get_settings

settings = get_settings()


async def generate(prompt: str) -> str:
    """Call the external LLM non-streaming endpoint and return the text."""
    if not settings.external_llm_url:
        raise RuntimeError("external_llm_url is not configured")

    payload = {"prompt": prompt}
    headers = {"Content-Type": "application/json"}
    if settings.external_llm_api_key:
        headers["Authorization"] = f"Bearer {settings.external_llm_api_key}"

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(settings.external_llm_url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    # Accept either {"text": "..."} or {"response": "..."}
    return data.get("text") or data.get("response") or json.dumps(data)


async def stream(prompt: str) -> AsyncGenerator[str, None]:
    """Call the external LLM streaming endpoint and yield tokens as they arrive.

    This function tries to be tolerant to common streaming protocols: SSE (text/event-stream)
    or newline-delimited JSON lines.
    """
    if not settings.external_llm_url:
        raise RuntimeError("external_llm_url is not configured")

    headers = {}
    if settings.external_llm_api_key:
        headers["Authorization"] = f"Bearer {settings.external_llm_api_key}"

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", settings.external_llm_url, json={"prompt": prompt}, headers=headers) as resp:
            resp.raise_for_status()
            content_type = resp.headers.get("content-type", "")

            # Server-Sent Events (SSE)
            if "text/event-stream" in content_type:
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    if line.startswith("data:"):
                        payload = line[len("data:"):].strip()
                        try:
                            obj = json.loads(payload)
                            token = obj.get("token") or obj.get("text") or payload
                        except Exception:
                            token = payload
                        yield token

            # Fallback: newline-delimited JSON objects or plain text chunks
            else:
                buffer = ""
                async for chunk in resp.aiter_text():
                    buffer += chunk
                    # try to split on newlines
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                            token = obj.get("token") or obj.get("text") or line
                        except Exception:
                            token = line
                        yield token
                # leftover
                if buffer:
                    yield buffer