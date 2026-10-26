from sqlalchemy.orm import Session
from ..models.case import Case
from ..models.task import Task
from ..models.document import Document

def dashboard_stats(db: Session):
    return {
        "total_cases": db.query(Case).count(),
        "open_cases": db.query(Case).filter(Case.status == "Open").count(),
        "closed_cases": db.query(Case).filter(Case.status == "Closed").count(),
        "pending_tasks": db.query(Task).filter(Task.completed == False).count(),
        "completed_tasks": db.query(Task).filter(Task.completed == True).count(),
        "documents": db.query(Document).count()
    }
