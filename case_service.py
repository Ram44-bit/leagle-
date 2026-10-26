from sqlalchemy.orm import Session
from ..models.case import Case

def list_cases(db: Session, search: str = "", status: str = ""):
    q = db.query(Case)
    if search:
        term = f"%{search.strip()}%"
        q = q.filter((Case.title.ilike(term)) | (Case.client_name.ilike(term)) | (Case.case_number.ilike(term)))
    if status:
        q = q.filter(Case.status == status)
    return q.order_by(Case.id.desc()).all()
