from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.analytics_service import dashboard_stats
from ..services.deadline_service import upcoming_deadlines

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    return dashboard_stats(db)

@router.get("/deadlines")
def deadlines(days: int = 30, db: Session = Depends(get_db)):
    days = max(1, min(days, 365))
    return upcoming_deadlines(db, days)
