# Validation Report

## Purpose

This document records the validation gates for Productive Failure Study Mode.

The project is a production-shaped local prototype. The validation proves application behaviour and regression safety, not real learning outcomes.

## Backend validation

Command:

```powershell
python -m pytest .\backend\tests
```

Expected healthy result at the Phase 5 baseline:

```text
20 passed
```

Coverage areas:

- health endpoint
- concept listing
- concept lookup
- unknown concept handling
- Pydantic failure-label enum closure
- session creation
- attempt submission
- consolidation response
- retrieval quiz generation
- answer key hidden before quiz submission
- quiz submission
- session trace
- local JSON persistence
- dashboard metrics
- CORS for local frontend
- eval runner behaviour

## Eval harness validation

Command:

```powershell
python -m app.evals.runner
```

Expected healthy summary:

```json
{
  "total_cases": 10,
  "passed_cases": 10,
  "failed_cases": 0,
  "pass_rate": 1.0
}
```

Eval checks:

- valid schema returned
- expected failure label or acceptable label set
- consolidation exists
- feedback is relevant to the failure label
- quiz has exactly 3 questions
- at least 1 transfer question exists
- answer key is not exposed before quiz submission
- skip-attempt direct-answer leakage guard

## Frontend validation

Commands:

```powershell
cd frontend
npm run typecheck
npm run build
cd ..
```

Expected healthy result:

```text
typecheck passes
Next.js build passes
```

## Browser smoke test

Backend:

```powershell
python -m uvicorn app.main:app --app-dir .\backend --reload
```

Frontend:

```powershell
cd frontend
npm run dev
```

Manual path:

1. Open `http://localhost:3000`.
2. Go to Learn.
3. Select Law: Offer and Acceptance.
4. Submit an imperfect attempt.
5. Confirm failure analysis appears.
6. Confirm consolidation appears.
7. Submit retrieval quiz.
8. Confirm quiz result appears.
9. Open dashboard.
10. Confirm metrics update.

## Privacy checks

Implemented posture:

- demo concepts only
- no real student data required
- aliases optional
- dashboard avoids exposing student alias
- local persistence by default
- no API key required
- no secrets committed

Not implemented yet:

- real consent flow
- account deletion workflow
- retention jobs
- encryption controls
- authentication
- role-based access control
- production audit trail

## Academic integrity checks

Implemented posture:

- attempt is required before consolidation
- answer key is hidden before quiz submission
- eval harness checks direct-answer leakage for skip-attempt behaviour
- UI frames the system as learning support

Not implemented yet:

- robust cheating intent classifier
- assessment-context detection
- uploaded assignment policy
- institution-specific academic-integrity rules

## Non-claims

Passing these validations does not prove:

- real student learning improvement
- Productive Failure efficacy in BAG Learning
- production readiness
- POPIA compliance
- live AI reliability
- scalability under real traffic

It proves:

```text
the local prototype implements the intended learning loop with typed contracts, deterministic mock AI, persistence, dashboard metrics, and regression-oriented eval checks.
```

## Phase 6.5 source-grounding validation

Additional validation added:

- sample course packs validate through `SampleCoursePack`
- every seeded concept has source provenance
- every concept has rubric items
- every concept has exactly three grounded retrieval questions
- every concept includes at least one transfer question
- attempt analysis returns matched and missing rubric items
- consolidation includes source provenance
- public quizzes include source provenance but not the hidden answer key
- eval harness remains deterministic and passes the fixed 10-case suite

Expected local gate after Phase 6.5:

```text
python -m pytest .\backend\tests
python -m app.evals.runner
cd frontend
npm run typecheck
npm run build
```
