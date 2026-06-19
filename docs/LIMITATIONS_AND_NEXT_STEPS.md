# Limitations and Next Steps

## Status label

Current status:

```text
production-shaped local prototype
```

Not production-ready.

## Non-claims

This project does not claim:

- Productive Failure improves BAG Learning outcomes
- the feature has been tested with real students
- the feature is production-ready
- the feature is POPIA compliant
- the feature replaces BAG Learning or Zazi
- the feature works for every subject without further validation
- the local dashboard is production analytics
- the mock engine is equivalent to live AI quality

Correct claim:

```text
This is a production-shaped feature spike showing how Productive Failure could be operationalized inside a BAG Learning-style AI study companion, with typed contracts, mock AI, local persistence, dashboard metrics, and an eval harness.
```

## Known limitations

### Mock AI

The learning engine is deterministic and rule-based. This is a good demo/eval boundary, but it does not represent final AI quality.

Next step:

```text
Add a LiveLearningEngine adapter that must satisfy the same Pydantic output contracts and eval gates.
```

### No RAG grounding

The current system uses seeded concepts. It does not ingest course material or ground responses in uploaded documents.

Next step:

```text
Add a retrieval boundary for uploaded course materials, then require source-backed challenges and consolidation.
```

### No real student outcome evaluation

The dashboard shows learning events, not learning efficacy.

Next step:

```text
Run a controlled study comparing attempt-first behaviour against explanation-first behaviour on delayed retrieval tasks.
```

### Local persistence only

The local JSON repository is useful for demonstration and adapter discipline. It is not a production storage layer.

Next step:

```text
Add Supabase/Postgres behind the existing LearningRepository protocol.
```

### No authentication

There is no real user authentication or account boundary.

Next step:

```text
Add authentication only after the core learning loop, storage model, and privacy controls are stable.
```

### No admin or institutional analytics

The dashboard is a student/demo dashboard, not an institution-level analytics system.

Next step:

```text
Design privacy-preserving aggregate analytics with data minimization and no raw attempt leakage.
```

## Privacy next steps

Before customer or student data:

1. Define data classification for attempts, quiz answers, aliases, and session metadata.
2. Add deletion workflow.
3. Add explicit consent copy for document processing.
4. Add retention configuration.
5. Avoid raw student attempts in logs.
6. Separate development and production storage.
7. Document vendor boundaries if live AI or managed database services are used.

## Academic integrity next steps

Before deployment:

1. Add stronger cheating-intent classification.
2. Refuse assessed-work completion requests.
3. Keep answer keys hidden until quiz submission.
4. Ground support in learning process, not final-answer generation.
5. Add UI copy that clearly states the product is for learning support.

## Product next steps inside BAG Learning

### Step 1: RAG-grounded concept mode

Use uploaded course material to generate or select the concept challenge.

Gate:

```text
challenge and consolidation cite retrieved source chunks
```

### Step 2: Spaced retrieval

Schedule follow-up retrieval prompts after the session.

Gate:

```text
student receives delayed retrieval question without seeing answer first
```

### Step 3: Learning outcome eval

Compare Attempt First Mode against normal explanation-first tutoring.

Gate:

```text
fixed delayed post-test cases show whether retention changed
```

### Step 4: Institution-level dashboard

Aggregate behaviour without exposing raw student attempts.

Gate:

```text
analytics show concept gaps without leaking personal learning data
```

### Step 5: Live AI adapter

Add a live model only after eval and refusal gates exist.

Gate:

```text
live output must pass schema validation and eval harness thresholds
```

## Commercial interpretation

For a reviewer, this project is not valuable because it is large. It is valuable because it is focused:

```text
one research-backed behaviour
one clear student problem
one end-to-end prototype
typed contracts
persistence
dashboard
evals
clear non-claims
```

That is the signal.
