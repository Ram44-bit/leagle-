from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.case import Case
from ..models.timeline import TimelineEvent
from ..services.case_service import list_cases

router = APIRouter(prefix="/api/cases", tags=["Cases"])

class CaseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    client_name: str = Field(min_length=1, max_length=160)
    case_number: str = ""
    court: str = ""
    case_type: str = "General"
    status: str = "Open"
    next_hearing: date | None = None
    notes: str = ""

class CaseUpdate(BaseModel):
    title: str | None = None
    client_name: str | None = None
    case_number: str | None = None
    court: str | None = None
    case_type: str | None = None
    status: str | None = None
    next_hearing: date | None = None
    notes: str | None = None

@router.get("")
def get_cases(search: str = "", status: str = "", db: Session = Depends(get_db)):
    return list_cases(db, search, status)

@router.post("", status_code=201)
def create_case(payload: CaseCreate, db: Session = Depends(get_db)):
    case = Case(**payload.model_dump())
    db.add(case); db.commit(); db.refresh(case)
    db.add(TimelineEvent(title="Case created", details=f"Case opened for {case.client_name}", event_date=date.today(), case_id=case.id))
    db.commit()
    return case

@router.get("/{case_id}")
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case: raise HTTPException(404, "Case not found")
    return case

@router.patch("/{case_id}")
def update_case(case_id: int, payload: CaseUpdate, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case: raise HTTPException(404, "Case not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(case, key, value)
    db.commit(); db.refresh(case)
    return case

@router.delete("/{case_id}", status_code=204)
def delete_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case: raise HTTPException(404, "Case not found")
    db.delete(case); db.commit()
