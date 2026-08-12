from fastapi import APIRouter
from schemas.history import SessionListResponse, SessionDetailResponse
from services.store import session_store

router = APIRouter()


@router.get("", response_model=SessionListResponse)
async def list_sessions():
    sessions = session_store.list_sessions()
    return SessionListResponse(sessions=sessions)


@router.get("/{session_id}", response_model=SessionDetailResponse)
async def get_session(session_id: str):
    messages = session_store.get_messages(session_id)
    return SessionDetailResponse(session_id=session_id, messages=messages)


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    session_store.delete_session(session_id)
    return {"deleted": session_id}
