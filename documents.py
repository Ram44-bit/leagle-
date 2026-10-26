from pathlib import Path
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..config import UPLOAD_DIR
from ..models.document import Document
from ..models.case import Case
from ..services.document_service import save_upload
from ..services.ai_service import extract_text_from_file, summarize_text

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.get("")
def list_documents(case_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(Document)
    if case_id: q = q.filter(Document.case_id == case_id)
    return q.order_by(Document.id.desc()).all()

@router.post("", status_code=201)
async def upload_document(case_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not db.query(Case).filter(Case.id == case_id).first():
        raise HTTPException(404, "Case not found")
    stored_name, size = await save_upload(file)
    doc = Document(original_name=file.filename or stored_name, stored_name=stored_name,
                   content_type=file.content_type or "application/octet-stream", size_bytes=size, case_id=case_id)
    db.add(doc); db.commit(); db.refresh(doc)
    return doc

@router.get("/{document_id}/download")
def download_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc: raise HTTPException(404, "Document not found")
    path = UPLOAD_DIR / doc.stored_name
    if not path.exists(): raise HTTPException(404, "Stored file not found")
    return FileResponse(path, filename=doc.original_name, media_type=doc.content_type)

@router.post("/{document_id}/summarize")
def summarize_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc: raise HTTPException(404, "Document not found")
    path = UPLOAD_DIR / doc.stored_name
    text = extract_text_from_file(path, Path(doc.original_name).suffix)
    if not text:
        raise HTTPException(400, "MVP summary supports .txt files only. PDF/DOCX text extraction can be added next.")
    return summarize_text(text)
