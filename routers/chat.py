"""
Chat router — handles prompt/response and SSE streaming.
"""
import asyncio
import json
import uuid
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from schemas.chat import ChatRequest, ChatResponse, ChatMessage
from services.llm import stub_llm_response, stub_stream_response
from services.store import session_store

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Send a prompt and receive a full response."""
    session_id = req.session_id or str(uuid.uuid4())
    reply = await stub_llm_response(req.prompt)

    user_msg = ChatMessage(role="user", content=req.prompt, timestamp=datetime.utcnow().isoformat())
    assistant_msg = ChatMessage(role="assistant", content=reply, timestamp=datetime.utcnow().isoformat())

    session_store.add_messages(session_id, [user_msg, assistant_msg])

    return ChatResponse(session_id=session_id, message=assistant_msg)


@router.get("/stream")
async def chat_stream(prompt: str, session_id: str = ""):
    """Stream a response token-by-token via Server-Sent Events."""
    sid = session_id or str(uuid.uuid4())

    async def event_generator():
        full_response = ""
        async for token in stub_stream_response(prompt):
            full_response += token
            data = json.dumps({"token": token, "session_id": sid})
            yield f"data: {data}\n\n"
            await asyncio.sleep(0)  # yield control

        # Save complete messages to history
        user_msg = ChatMessage(role="user", content=prompt, timestamp=datetime.utcnow().isoformat())
        assistant_msg = ChatMessage(role="assistant", content=full_response, timestamp=datetime.utcnow().isoformat())
        session_store.add_messages(sid, [user_msg, assistant_msg])

        # Send done event
        yield f"data: {json.dumps({'done': True, 'session_id': sid})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
