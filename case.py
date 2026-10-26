from sqlalchemy import String, Text, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base

class Case(Base):
    __tablename__ = "cases"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    client_name: Mapped[str] = mapped_column(String(160), index=True)
    case_number: Mapped[str] = mapped_column(String(100), default="")
    court: Mapped[str] = mapped_column(String(160), default="")
    case_type: Mapped[str] = mapped_column(String(100), default="General")
    status: Mapped[str] = mapped_column(String(40), default="Open", index=True)
    next_hearing: Mapped[Date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    tasks = relationship("Task", back_populates="case", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")
    timeline = relationship("TimelineEvent", back_populates="case", cascade="all, delete-orphan")
