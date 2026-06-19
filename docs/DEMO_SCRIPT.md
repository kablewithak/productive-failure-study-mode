# Demo Script: Five-Minute Reviewer Walkthrough

## Demo objective

Show that Attempt First Mode is a working, production-shaped feature spike:

```text
student attempt
→ failure analysis
→ consolidation
→ retrieval quiz
→ dashboard event
```

Do not try to show every page or every file. The goal is a clean reviewer path.

## Pre-demo setup

Open two PowerShell tabs.

### Backend tab

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --app-dir .\backend --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

### Frontend tab

```powershell
cd frontend
npm run dev
```

Open:

```text
http://localhost:3000
```

## Spoken framing

Use this:

```text
Most AI study tools explain too quickly. This prototype tests a different learning behaviour: the student must attempt before receiving the full explanation.

The goal is not to clone BAG Learning or Zazi. The goal is to show how Productive Failure could become a concrete study mode inside a BAG-style AI companion.

The demo is mock-AI first, so it runs without API keys. The serious part is the harness: typed contracts, persistence, dashboard metrics, and eval cases.
```

## Demo path

### 1. Home page

Show the north star:

```text
Attempt first. Fail safely. Consolidate. Practise retrieval.
```

Say:

```text
The interface frames failure as diagnostic learning evidence, not as shame.
```

### 2. Learn page

Open:

```text
http://localhost:3000/learn
```

Show that concepts span disciplines:

- Law
- Commerce
- Engineering
- Programming

Say:

```text
This is intentionally not a Python tutor. Python is only included because the paper’s demonstration case uses Python lists.
```

### 3. Select Law: Offer and Acceptance

Choose the law concept.

Say:

```text
I’m choosing law first because it proves the abstraction works outside programming.
```

### 4. Submit imperfect attempt

Use this attempt:

```text
I think acceptance happens when both people agree somehow, but I am not sure when it becomes legally valid.
```

Confidence:

```text
2
```

Confusion note:

```text
I am not sure when acceptance becomes legally valid.
```

Submit.

### 5. Show failure analysis

Point out:

- failure label
- prior knowledge detected
- missing concept
- misconception summary
- productive failure score
- feedback strategy

Say:

```text
This is the key AI engineering boundary. The model-shaped output is not a vague paragraph. It becomes structured application data.
```

### 6. Show consolidation

Point out:

- acknowledgement
- what was useful
- missing or confused points
- explanation
- worked example
- immediate retrieval prompt

Say:

```text
The explanation appears only after the attempt. The system rewards learning behaviour, not passive answer consumption.
```

### 7. Show retrieval quiz

Submit answers. Imperfect answers are fine.

Say:

```text
The quiz turns the consolidation into active retrieval instead of ending at explanation.
```

### 8. Show dashboard

Open:

```text
http://localhost:3000/dashboard
```

Point out:

- total sessions
- completed sessions
- average confidence
- average quiz score
- failure labels
- recent events
- concepts attempted

Say:

```text
This is not production analytics. It proves the learning-event data model and product loop.
```

### 9. Show code quickly

Open these files:

```text
backend/app/models.py
backend/app/main.py
backend/app/services/mock_learning_engine.py
backend/app/repositories/base.py
backend/app/evals/cases.py
```

Say:

```text
The architecture is local-first and provider-neutral. A live AI engine or Supabase repository can be added behind existing seams without rewriting the product flow.
```

## Close

Use this:

```text
The correct claim is narrow: this is a production-shaped feature spike. It does not prove real learning outcomes yet. The next step would be grounding challenges in uploaded course material, adding citations, and running a real learning-outcome evaluation.
```

## Demo failure fallback

If frontend fails:

1. Open backend docs.
2. Use `POST /sessions`.
3. Use `POST /sessions/{session_id}/attempt`.
4. Use `POST /sessions/{session_id}/quiz`.
5. Use `GET /dashboard`.

Say:

```text
The browser UI is the demo surface. The backend contract is the core product behaviour.
```
