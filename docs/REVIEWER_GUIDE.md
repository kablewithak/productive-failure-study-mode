# Reviewer Guide

## Three-minute inspection path

Start here if you are reviewing the project quickly.

## 1. Read the north star

Open:

```text
README.md
```

Look for:

```text
Attempt first before explanation.
```

The project is not trying to be a full BAG Learning clone. It is a focused feature spike.

## 2. Run the app

Backend:

```powershell
python -m uvicorn app.main:app --app-dir .\backend --reload
```

Frontend:

```powershell
cd frontend
npm run dev
```

Open:

```text
http://localhost:3000
```

## 3. Demo the learning loop

Use:

```text
Law: Offer and Acceptance
```

Submit:

```text
I think acceptance happens when both people agree somehow, but I am not sure when it becomes legally valid.
```

Expected behaviour:

```text
attempt
→ failure analysis
→ targeted consolidation
→ retrieval quiz
→ dashboard event
```

## 4. Inspect the engineering boundaries

Open:

```text
backend/app/models.py
```

Look for:

- Pydantic models
- closed enums
- `FailureAnalysis`
- `ConsolidationResponse`
- `RetrievalQuiz`

Open:

```text
backend/app/services/mock_learning_engine.py
```

Look for deterministic mock AI-shaped behaviour.

Open:

```text
backend/app/repositories/base.py
```

Look for the repository boundary.

Open:

```text
backend/app/evals/cases.py
```

Look for fixed diagnostic eval cases.

## 5. Run validation

```powershell
python -m pytest .\backend\tests
python -m app.evals.runner
cd frontend
npm run typecheck
npm run build
cd ..
```

## 6. Judge the right thing

Judge this project on:

- product translation
- typed contracts
- attempt-first enforcement
- local-first maintainability
- eval discipline
- privacy posture
- honest non-claims

Do not judge it as:

- a full production deployment
- a full BAG Learning clone
- a real learning-outcome study
- a live AI quality benchmark
- a finished institutional analytics product

## Strongest signal

The strongest signal is not that the app is large.

The strongest signal is that the repo shows how to convert research into inspectable product behaviour:

```text
research sequence
→ product loop
→ typed contracts
→ deterministic mock engine
→ persistence
→ dashboard evidence
→ eval regression checks
```
