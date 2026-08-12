from models.chat import ChatMessage
from models.history import SessionSummary
from models.feedback import FeedbackRequest
from typing import List, Dict
from datetime import datetime


class InMemoryStore:
    """Simple in-memory store — replace with PostgreSQL later."""

    def __init__(self):
        self._sessions: Dict[str, List[ChatMessage]] = {}
        self._feedback: List[dict] = []
        self._created_at: Dict[str, str] = {}

    # ── Sessions ──────────────────────────────────────────────────────────────

    def add_messages(self, session_id: str, messages: List[ChatMessage]):
        if session_id not in self._sessions:
            self._sessions[session_id] = []
            self._created_at[session_id] = datetime.utcnow().isoformat()
        self._sessions[session_id].extend(messages)

    def get_messages(self, session_id: str) -> List[ChatMessage]:
        return self._sessions.get(session_id, [])

    def list_sessions(self) -> List[SessionSummary]:
        result = []
        for sid, msgs in self._sessions.items():
            last = msgs[-1].content[:80] + "..." if len(msgs[-1].content) > 80 else msgs[-1].content
            result.append(SessionSummary(
                session_id=sid,
                message_count=len(msgs),
                last_message=last,
                created_at=self._created_at.get(sid, ""),
            ))
        return sorted(result, key=lambda s: s.created_at, reverse=True)

    def delete_session(self, session_id: str):
        self._sessions.pop(session_id, None)
        self._created_at.pop(session_id, None)

    # ── Feedback ──────────────────────────────────────────────────────────────

    def add_feedback(self, feedback: FeedbackRequest):
        self._feedback.append(feedback.model_dump())

    def list_feedback(self) -> List[dict]:
        return self._feedback


session_store = InMemoryStore()
