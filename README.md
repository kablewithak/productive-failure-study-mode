# Productive Failure Study Mode

Production-shaped feature spike for a BAG Learning-style AI study companion.

## North Star

Build a discipline-agnostic **Attempt First Mode** where a South African university student must try a short challenge before receiving the full explanation.

The learning loop is:

```text
select concept
→ attempt pre-instruction challenge
→ submit confidence and confusion note
→ receive structured failure analysis
→ receive targeted consolidation
→ complete retrieval quiz
→ review learning-event dashboard
```

This is not a Python tutor. Python lists are included because the research demonstration case is Productive Failure for introductory Python programming. The product behaviour is meant to generalize across university disciplines such as law, commerce, engineering, statistics, actuarial science, and computer science.

## What this proves

This repository demonstrates that the builder can convert learning-science research into a working product behaviour:

- a student must attempt before the system explains
- AI-shaped outputs are represented through typed contracts
- mock AI mode is deterministic and does not require API keys
- learning events persist locally through a repository adapter
- the dashboard reports learning behaviour metrics
- fixed eval cases check regression-prone AI behaviour
- the browser flow works end to end against a FastAPI backend

## What this does not prove

This project does not prove that Productive Failure improves BAG Learning outcomes.

It is not production-ready.
It is not POPIA compliant.
It does not replace BAG Learning or Zazi.
It has not been tested with real students.
It does not use real course uploads or copyrighted university material. It uses bundled sample course packs written specifically for this demo.

Correct claim:

> This is a production-shaped feature spike showing how Productive Failure could be operationalized inside a BAG Learning-style AI study companion, with typed contracts, mock AI, local persistence, dashboard metrics, and an eval harness.

## Stack

| Layer | Choice |
|---|---|
| Frontend | Next.js, React, TypeScript, Tailwind |
| Backend | FastAPI, Pydantic v2 |
| Persistence | Local JSON adapter behind repository boundary |
| AI mode | Deterministic source-grounded mock learning engine |
| Eval harness | Fixed diagnostic cases against mock engine |
| Local development | Windows PowerShell, VS Code, GitHub |

## Repository layout

```text
productive-failure-study-mode/
  backend/
    app/
      evals/
      repositories/
      services/
      concept_seed.py
      main.py
      models.py
      settings.py
      time_utils.py
    tests/
    pyproject.toml
  frontend/
    app/
    components/
    lib/
    package.json
  docs/
    PRD.md
    RESEARCH_MAPPING.md
    ARCHITECTURE.md
    DEMO_SCRIPT.md
    LIMITATIONS_AND_NEXT_STEPS.md
    VALIDATION_REPORT.md
    REVIEWER_GUIDE.md
  README.md
```

## Local setup

Clone the repository:

```powershell
git clone https://github.com/kablewithak/productive-failure-study-mode.git
cd productive-failure-study-mode
```

Create and activate the Python environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip
python -m pip install -e ".\backend[dev]"
```

Install frontend dependencies:

```powershell
cd frontend
npm install
cd ..
```


## Python environment troubleshooting

This project has been validated with Python 3.11.

If the backend fails with an error like:

```text
ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'
```

the virtual environment is probably stale, corrupted, or created with a different Python version. Delete and recreate it with Python 3.11:

```powershell
deactivate
Remove-Item ".\.venv" -Recurse -Force
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip
python -m pip install -e ".\backend[dev]"
```

Expected Python version:

```text
Python 3.11.x
```

## Run the backend

```powershell
python -m uvicorn app.main:app --app-dir .\backend --reload
```

Open:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
http://127.0.0.1:8000/concepts
http://127.0.0.1:8000/dashboard
```

Expected health response:

```json
{
  "status": "ok",
  "service": "productive-failure-api"
}
```

## Run the frontend

Open a second PowerShell tab:

```powershell
cd productive-failure-study-mode
.\.venv\Scripts\Activate.ps1
cd frontend
npm run dev
```

Open:

```text
http://localhost:3000
```

## Five-minute demo path

Use the Law concept first because it proves the system is not just a Python tutor.

1. Open the home page.
2. Go to **Learn**.
3. Select **Law: Offer and Acceptance**.
4. Submit an imperfect attempt:
   ```text
   I think acceptance happens when both people agree somehow, but I am not sure when it becomes legally valid.
   ```
5. Show the failure analysis.
6. Show the targeted consolidation.
7. Complete the retrieval quiz.
8. Open the dashboard and show the updated learning event.
9. Briefly open the code:
   - `backend/app/models.py`
   - `backend/app/main.py`
   - `backend/app/services/mock_learning_engine.py`
   - `backend/app/evals/cases.py`

## Validation

Backend:

```powershell
python -m pytest .\backend\tests
```

Eval harness:

```powershell
python -m app.evals.runner
```

Frontend:

```powershell
cd frontend
npm run typecheck
npm run build
cd ..
```

## Documentation map

| Document | Purpose |
|---|---|
| `docs/PRD.md` | Original product and build contract |
| `docs/RESEARCH_MAPPING.md` | Maps BAG Learning context and Productive Failure research to product behaviour |
| `docs/ARCHITECTURE.md` | Explains boundaries, contracts, services, repositories, and eval harness |
| `docs/DEMO_SCRIPT.md` | Gives the exact reviewer demo path |
| `docs/LIMITATIONS_AND_NEXT_STEPS.md` | States non-claims, risks, and production next steps |
| `docs/VALIDATION_REPORT.md` | Lists implemented validation gates and commands |
| `docs/REVIEWER_GUIDE.md` | Helps a reviewer inspect the project quickly |

## Privacy and academic-integrity posture

This prototype uses demo concepts only. It does not require real student names, real student records, uploaded course materials, or API keys.

The intended academic posture is:

> This mode is designed to help students learn by attempting first, receiving feedback, and practising retrieval. It is not designed to complete assessed work for students.

## Next production-shaped steps

1. Replace bundled sample course packs with a real upload/RAG boundary.
2. Add retrieval ranking, citations, and unsupported fallback behaviour.
3. Add spaced retrieval follow-ups after the first session.
4. Add Supabase/Postgres persistence behind the existing repository contract.
5. Add real student outcome evals before making learning-effectiveness claims.
