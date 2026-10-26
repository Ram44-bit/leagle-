from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from . import models
from .api import cases, tasks, documents, analytics, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Legal Case Manager API",
    description="Hackathon MVP for case tracking, document organization, task management and deadline overview.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cases.router)
app.include_router(tasks.router)
app.include_router(documents.router)
app.include_router(analytics.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"name": "Legal Case Manager API", "status": "running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"ok": True}
