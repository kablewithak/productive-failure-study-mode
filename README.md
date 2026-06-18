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
- Persistence: local adapter first, Supabase/Postgres optional
- AI mode: deterministic mock AI first, optional live AI later
- Evals: fixed cases for failure labels, consolidation, retrieval quiz shape, and answer-key leakage

## Non-claims

This prototype does not prove real learning outcomes.
It is not production-ready.
It is not POPIA compliant.
It does not replace BAG Learning or Zazi.
It is a production-shaped feature spike.

## First delivery gate

Phase 0 is complete when:

- repo exists
- first commit is pushed
- README states the north star
- docs/PRD.md exists
- frontend and backend folders exist
- .env.example exists
- .gitignore exists
