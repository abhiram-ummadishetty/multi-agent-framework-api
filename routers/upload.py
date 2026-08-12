"""
Upload router — handles file uploads.
"""
import os
import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException
from models.upload import UploadResponse
from config import get_settings

router = APIRouter()



@router.post("", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload a file and return metadata."""
    settings = get_settings()
    upload_dir = settings.upload_dir
    max_size_mb = settings.max_upload_size_mb

    content = await file.read()

    if len(content) > max_size_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File exceeds {max_size_mb}MB limit")

    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename or "")[1]
    saved_name = f"{file_id}{ext}"
    save_path = os.path.join(upload_dir, saved_name)

    os.makedirs(upload_dir, exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(content)

    return UploadResponse(
        file_id=file_id,
        filename=file.filename or saved_name,
        size_bytes=len(content),
        content_type=file.content_type or "application/octet-stream",
        uploaded_at=datetime.utcnow().isoformat(),
        path=save_path,
    )

