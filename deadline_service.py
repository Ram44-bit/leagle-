from datetime import date, timedelta
from sqlalchemy.orm import Session
from ..models.case import Case
from ..models.task import Task

def upcoming_deadlines(db: Session, days: int = 30):
    today = date.today()
    until = today + timedelta(days=days)
    hearings = db.query(Case).filter(Case.next_hearing >= today, Case.next_hearing <= until).all()
    tasks = db.query(Task).filter(Task.completed == False, Task.due_date >= today, Task.due_date <= until).all()
    return {
        "hearings": [{"case_id": c.id, "case_title": c.title, "date": c.next_hearing.isoformat()} for c in hearings],
        "tasks": [{"task_id": t.id, "title": t.title, "case_id": t.case_id, "date": t.due_date.isoformat()} for t in tasks]
    }
