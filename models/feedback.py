from pydantic import BaseModel
from typing import Optional
import uuid


class FeedbackRequest(BaseModel):
    feedback_id: str = ""
    session_id: str
    message_id: Optional[str] = None
    rating: int  # 1 = thumbs up, -1 = thumbs down
    comment: Optional[str] = None

    def model_post_init(self, __context):
        if not self.feedback_id:
            self.feedback_id = str(uuid.uuid4())


class FeedbackResponse(BaseModel):
    feedback_id: str
    status: str
