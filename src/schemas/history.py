from pydantic import BaseModel
from typing import List
from schemas.chat import ChatMessage


class SessionSummary(BaseModel):
    session_id: str
    message_count: int
    last_message: str
    created_at: str


class SessionListResponse(BaseModel):
    sessions: List[SessionSummary]


class SessionDetailResponse(BaseModel):
    session_id: str
    messages: List[ChatMessage]


__all__ = ["SessionListResponse", "SessionDetailResponse", "SessionSummary", "ChatMessage"]
