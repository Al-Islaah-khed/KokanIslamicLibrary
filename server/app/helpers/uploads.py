from fastapi import UploadFile, HTTPException, status
from pathlib import Path
import os
from uuid import uuid4

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 1 * 1024 * 1024  # 500kb default max size

def upload_image(
    upload_dir: Path,
    file: UploadFile,
    base_url: str,
    max_size: int = MAX_FILE_SIZE
) -> str:
    # Check extension
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only image files {', '.join(ALLOWED_EXTENSIONS)} are allowed"
        )

    # Check size
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)  # reset pointer

    if size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {max_size / (1024*1024)} MB"
        )

    # Save file
    filename = f"{uuid4().hex}{ext}"
    filepath = upload_dir / filename

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    # Return accessible URL path
    return f"{base_url}/public/uploads/profile-images/{filename}"
