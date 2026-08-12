from typing import List, Optional
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from db.models import ChatThread, ChatMessage as ChatMessageModel, Feedback as FeedbackModel
from db.session import AsyncSessionLocal
from schemas.chat import ChatMessage
from schemas.feedback import FeedbackRequest
from schemas.history import SessionSummary


class DatabaseStore:
    """PostgreSQL-backed session and feedback store."""

    async def _get_or_create_thread(self, session, session_id: str, user_id: Optional[str] = None) -> ChatThread:
        result = await session.scalar(
            select(ChatThread).where(ChatThread.session_id == session_id)
        )
        if result:
            return result

        thread = ChatThread(session_id=session_id, user_id=user_id)
        session.add(thread)
        await session.flush()
        return thread

    async def add_messages(self, session_id: str, messages: List[ChatMessage], user_id: Optional[str] = None):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                thread = await self._get_or_create_thread(session, session_id, user_id)
                for message in messages:
                    db_message = ChatMessageModel(
                        thread_id=thread.id,
                        role=message.role,
                        content=message.content,
                        message_id=message.message_id,
                    )
                    session.add(db_message)

    async def get_messages(self, session_id: str) -> List[ChatMessage]:
        async with AsyncSessionLocal() as session:
            result = await session.scalar(
                select(ChatThread).options(selectinload(ChatThread.messages)).where(ChatThread.session_id == session_id)
            )
            if not result:
                return []
            return [
                ChatMessage(
                    role=message.role,
                    content=message.content,
                    timestamp=message.created_at.isoformat(),
                    message_id=message.message_id,
                )
                for message in result.messages
            ]

    async def list_sessions(self) -> List[SessionSummary]:
        async with AsyncSessionLocal() as session:
            result = await session.scalars(
                select(ChatThread).options(selectinload(ChatThread.messages)).order_by(ChatThread.created_at.desc())
            )
            sessions = []
            for thread in result.unique().all():
                if not thread.messages:
                    continue
                last_message = thread.messages[-1]
                last_text = last_message.content
                if len(last_text) > 80:
                    last_text = last_text[:80] + "..."
                sessions.append(
                    SessionSummary(
                        session_id=thread.session_id,
                        message_count=len(thread.messages),
                        last_message=last_text,
                        created_at=thread.created_at.isoformat(),
                    )
                )
            return sessions

    async def delete_session(self, session_id: str):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                await session.execute(delete(ChatThread).where(ChatThread.session_id == session_id))

    async def add_feedback(self, feedback: FeedbackRequest):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                session.add(
                    FeedbackModel(
                        feedback_id=feedback.feedback_id,
                        session_id=feedback.session_id,
                        message_id=feedback.message_id,
                        rating=feedback.rating,
                        comment=feedback.comment,
                    )
                )

    async def list_feedback(self) -> List[dict]:
        async with AsyncSessionLocal() as session:
            result = await session.scalars(select(FeedbackModel))
            return [
                {
                    "feedback_id": row.feedback_id,
                    "session_id": row.session_id,
                    "message_id": row.message_id,
                    "rating": row.rating,
                    "comment": row.comment,
                    "created_at": row.created_at.isoformat() if row.created_at else None,
                }
                for row in result.all()
            ]


session_store = DatabaseStore()
