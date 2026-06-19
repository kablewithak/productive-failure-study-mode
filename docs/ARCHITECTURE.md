# Architecture: Productive Failure Study Mode

## Architecture goal

The system is built as a production-shaped feature spike, not a toy prompt demo.

The important boundary is:

```text
LLM-shaped behaviour must become typed application data before the rest of the system uses it.
```

## System map

```text
Next.js frontend
  → typed API client
  → FastAPI backend
  → Pydantic contracts
  → mock learning engine
  → repository adapter
  → local JSON persistence
  → dashboard metrics
  → eval harness
```

## Frontend

Location:

```text
frontend/
```

Responsibilities:

- render home page
- show concept cards
- create learning sessions
- collect student attempts
- show failure analysis after attempt
- show consolidation after analysis
- submit retrieval quiz answers
- render dashboard metrics
- explain the project on the about page

The frontend does not own learning logic. It calls the backend and renders typed responses.

## Backend

Location:

```text
backend/app/
```

Core files:

| File | Responsibility |
|---|---|
| `main.py` | FastAPI routes and API composition |
| `models.py` | Pydantic v2 contracts and enums |
| `concept_seed.py` | Fixed demo concept library |
| `settings.py` | Environment-driven settings |
| `time_utils.py` | Shared UTC timestamp utility |
| `services/mock_learning_engine.py` | Deterministic mock AI-shaped behaviour |
| `repositories/base.py` | Repository protocol |
| `repositories/memory.py` | In-memory adapter for tests/local work |
| `repositories/json_file.py` | Local JSON persistence adapter |
| `evals/cases.py` | Fixed eval cases |
| `evals/runner.py` | Eval runner and pass/fail report |

## API surface

Implemented endpoints:

```text
GET  /health
GET  /concepts
GET  /concepts/{concept_id}
POST /sessions
POST /sessions/{session_id}/attempt
POST /sessions/{session_id}/quiz
GET  /sessions/{session_id}
GET  /dashboard
```

## Data contracts

All AI-shaped outputs are represented as Pydantic models:

- `FailureAnalysis`
- `ConsolidationResponse`
- `RetrievalQuiz`
- `QuizResultFeedback`

Failure labels are closed enum values. This matters because downstream UI, dashboard metrics, and evals should not depend on vague model text.

## Mock learning engine

The mock learning engine is deliberately deterministic.

Reasons:

- demo works without API keys
- eval harness can run reliably
- reviewer can inspect behaviour without vendor access
- failure labels are reproducible
- baseline regression checks are stable

This is not meant to be the final intelligence layer. It is the harness boundary that a live model would need to satisfy later.

## Persistence boundary

The route handlers do not directly own storage details.

They use a repository boundary:

```text
LearningRepository
```

Current adapters:

- memory repository
- local JSON repository

This keeps the v1 demo local-first while preserving a future seam for Supabase/Postgres.

## Dashboard metrics

The dashboard is based on persisted learning events, not fake analytics.

It reports:

- total sessions
- completed sessions
- average confidence score
- average quiz score
- failure label distribution
- recent learning events
- concepts attempted

The dashboard deliberately avoids exposing student aliases.

## Eval harness

The eval harness checks behaviour that is easy to break during AI iterations:

- valid schema output
- expected failure labels
- consolidation exists
- quiz has exactly 3 questions
- at least 1 transfer question exists
- answer key is not exposed before quiz submission
- skip-attempt answer-seeking behaviour does not leak a direct answer

The eval harness is not a learning-outcome study. It is a regression gate for application behaviour.

## Privacy and security posture

This prototype models sane controls:

- demo concepts only
- no real student data required
- aliases instead of real identities
- no API keys required
- local persistence only by default
- no secrets committed
- dashboard avoids student alias leakage

This is POPIA-aligned engineering posture, not a POPIA compliance claim.

## Extension seams

The next durable seams are:

1. `LiveLearningEngine` behind the same output contracts.
2. `SupabaseLearningRepository` or `PostgresLearningRepository` behind the repository protocol.
3. RAG-grounded concept/challenge generation.
4. Citation/provenance fields on challenge and consolidation outputs.
5. Scheduled spaced retrieval events.
6. Institution-level analytics with privacy controls.

## Phase 6.5 source-grounded sample course packs

The prototype now uses bundled sample course packs as the source-of-truth layer for the deterministic learning flow. This is intentionally smaller than a full upload/RAG pipeline.

New boundary:

```text
sample_course_packs/*.json
  → SampleCoursePack validation
  → Concept seed contract
  → rubric-based attempt analysis
  → source-grounded consolidation
  → source-grounded retrieval quiz
  → hidden answer key used only at quiz submission
```

The course packs contain sample source excerpts, rubric criteria, expected markers, canonical answers, worked examples, and retrieval question answer keys. The frontend exposes source provenance such as `Sample Law Notes §1`, but the API still hides quiz answer keys before quiz submission.

This improves the demo logic without pretending to support arbitrary student uploads. Full document ingestion, chunking, retrieval, citation ranking, and unsupported-answer fallback remain future work.
