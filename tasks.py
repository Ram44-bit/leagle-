from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.task import Task
from ..models.case import Case

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    due_date: date | None = None
    priority: str = "Medium"
    case_id: int | None = None

@router.get("")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.completed.asc(), Task.due_date.asc()).all()

@router.post("", status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    if payload.case_id and not db.query(Case).filter(Case.id == payload.case_id).first():
        raise HTTPException(404, "Linked case not found")
    task = Task(**payload.model_dump())
    db.add(task); db.commit(); db.refresh(task)
    return task

@router.patch("/{task_id}/toggle")
def toggle_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task: raise HTTPException(404, "Task not found")
    task.completed = not task.completed
    db.commit(); db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task: raise HTTPException(404, "Task not found")
    db.delete(task); db.commit()
