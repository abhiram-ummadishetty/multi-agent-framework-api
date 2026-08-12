from pydantic import BaseModel
from typing import Optional


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: str
    message_id: Optional[str] = None


class ChatRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = None
    agent_id: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    message: ChatMessage


__all__ = ["ChatMessage", "ChatRequest", "ChatResponse"]
