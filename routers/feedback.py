"""
Feedback router — thumbs up/down + text feedback per message.
"""
from fastapi import APIRouter
from models.feedback import FeedbackRequest, FeedbackResponse
from services.store import session_store

router = APIRouter()


@router.post("", response_model=FeedbackResponse)
async def submit_feedback(req: FeedbackRequest):
    """Submit feedback for an assistant message."""
    session_store.add_feedback(req)
    return FeedbackResponse(
        feedback_id=req.feedback_id,
        status="received",
    )


@router.get("")
async def list_feedback():
    """List all feedback entries (for admin/review)."""
    return {"feedback": session_store.list_feedback()}
