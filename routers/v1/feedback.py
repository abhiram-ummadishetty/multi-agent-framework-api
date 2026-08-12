from fastapi import APIRouter
from schemas.feedback import FeedbackRequest, FeedbackResponse
from services.store import session_store

router = APIRouter()


@router.post("", response_model=FeedbackResponse)
async def submit_feedback(req: FeedbackRequest):
    session_store.add_feedback(req)
    return FeedbackResponse(feedback_id=req.feedback_id, status="received")


@router.get("")
async def list_feedback():
    return {"feedback": session_store.list_feedback()}
