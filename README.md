# Productive Failure Study Mode

Production-shaped feature spike for a BAG Learning-style AI study companion.

## North Star

Build a discipline-agnostic **Attempt First Mode** where a university student must try a short challenge before receiving the full explanation.

The learning loop:

1. Select a concept.
2. Attempt a pre-instruction challenge.
3. Submit confidence and confusion note.
4. Receive structured failure analysis.
5. Receive targeted consolidation.
6. Complete a retrieval quiz.
7. Review learning-event dashboard.

## Why this exists

Most AI study tools explain too quickly. This prototype tests a different learning behaviour: useful friction before explanation.

It is inspired by Productive Failure research, where learners first attempt a novel problem before consolidation instruction. The referenced study found similar initial performance between Productive Failure and Direct Instruction, but stronger delayed retention for the Productive Failure group in its tested Python-list setup.

## Stack

- Frontend: Next.js, React, TypeScript, Tailwind
- Backend: FastAPI, Pydantic v2
- Persistence: local JSON adapter first, Supabase/Postgres optional later
- AI mode: deterministic mock AI first, optional live AI later
- Evals: fixed cases for failure labels, consolidation, retrieval quiz shape, and answer-key leakage

## Local run

### Backend

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".\backend[dev]"
python -m uvicorn app.main:app --app-dir .\backend --reload
```

Backend API:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/dashboard
```

### Frontend

Open a second PowerShell tab from the repo root.

```powershell
Set-Location "C:\Users\kabom\Documents\Machine Learning\Machine Learning Workspace\productive-failure-study-mode"
cd frontend
npm install
npm run dev
```

Frontend app:

```text
http://localhost:3000
```

## Validation

```powershell
python -m pytest .\backend\tests
cd frontend
npm run typecheck
npm run build
```

## Non-claims

This prototype does not prove real learning outcomes.
It is not production-ready.
It is not POPIA compliant.
It does not replace BAG Learning or Zazi.
It is a production-shaped feature spike.
