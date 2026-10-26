from pathlib import Path
from ..config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_UPLOAD_BYTES
from fastapi import HTTPException, UploadFile
import uuid

async def save_upload(file: UploadFile):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type. Allowed: PDF, DOC/DOCX, TXT, PNG, JPG.")
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the 15 MB upload limit.")
    stored_name = f"{uuid.uuid4().hex}{suffix}"
    (UPLOAD_DIR / stored_name).write_bytes(data)
    return stored_name, len(data)
