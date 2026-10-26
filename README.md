# Legal Case Manager — Hackathon MVP

A starter web app for lawyers to organize cases, track hearing dates, manage tasks, and upload case documents. It uses FastAPI + SQLite for the backend and React + Vite for the frontend.

## Features
- Dashboard counts for cases, tasks, and upcoming hearings
- Create, search, view, and update cases
- Create and complete tasks linked to cases
- Upload and list documents linked to cases
- Simple AI-ready case/document summary endpoint (rule-based fallback; no legal advice)
- SQLite database created automatically

## Run locally
Requirements: Python 3.10+ and Node.js 18+.

### 1. Start backend
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend API: http://127.0.0.1:8000  
API docs: http://127.0.0.1:8000/docs

### 2. Start frontend in another terminal
```bash
cd frontend
npm install
npm run dev
```
Open the URL printed by Vite (usually http://localhost:5173).

## Docker (optional)
From the project root:
```bash
docker compose up --build
```
Frontend: http://localhost:5173, API: http://localhost:8000

## Important
- This is a hackathon prototype, not production-ready legal software.
- Do not upload confidential client documents to a public demo without authorization.
- The summary feature is organizational assistance, not legal advice. A lawyer must verify all extracted facts, dates, and conclusions.
- Authentication, role-based permissions, encrypted file storage, backups, audit logging, and production-grade validation should be added before real client use.
