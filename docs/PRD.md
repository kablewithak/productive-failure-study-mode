# Product Requirements Document: Productive Failure Study Mode

**Project codename:** PF-Zazi / Attempt First Mode  
**Artifact type:** Build PRD + LLM handoff contract  
**Target company context:** BAG Learning, South African EdTech  
**Target role context:** 15-hour/week developer internship, production-feature mindset  
**Primary builder environment:** Windows, PowerShell, VS Code, GitHub  
**Time constraint for first build:** approximately 12 hours  

---

## 1. North Star

Build a **discipline-agnostic Productive Failure study mode** that shows how BAG Learning could help any South African university student attempt, fail safely, receive targeted consolidation, and practise retrieval before exams.

This is not a Python tutor. Python is only one research-backed demonstration case because the Productive Failure paper studies introductory Python lists. The actual product concept must generalize across law, commerce, engineering, statistics, actuarial science, and other university modules.

The core learning loop is:

```text
Any university concept
  → pre-instruction challenge
  → student attempt
  → failure-pattern analysis
  → targeted consolidation
  → retrieval quiz
  → learning event dashboard
```

The project must prove four things:

1. The builder understands BAG Learning's education problem.
2. The builder can translate learning-science research into product behaviour.
3. The builder can ship in a modern web stack: Next.js, React, Tailwind, FastAPI, Supabase/Postgres.
4. The builder can build AI features with typed contracts, evals, and clear reliability boundaries.

---

## 2. Strategic Intent

BAG Learning already appears to position itself around helping South African university students study better through AI-supported notes, quizzes, tutoring, language simplification, and structured study support.

This project proposes a focused extension:

> Instead of Zazi or any AI tutor explaining first, the system makes the student try first.

The feature should turn an AI tutor from a passive explanation machine into a **learning-behaviour engine**.

Most AI study tools give answers too quickly. That can make students feel productive while skipping the cognitive work needed for durable learning. Productive Failure Study Mode introduces useful friction: the learner must attempt a concept before receiving the full explanation.

The product bet:

> Students learn more deeply when the AI tutor sequences struggle, feedback, consolidation, and retrieval instead of immediately giving polished explanations.

---

## 3. Research Basis

### 3.1 Productive Failure

Productive Failure is an instructional approach where learners first attempt a novel problem targeting concepts they have not yet fully learned. Only after that attempt do they receive instruction or consolidation.

The referenced Productive Failure paper investigates this approach for undergraduate students learning Python lists. Its useful product insight is not that BAG Learning should become a Python tool. The useful insight is the learning sequence:

```text
Problem-solving before instruction
  → visible attempt
  → failure or partial success
  → consolidation instruction
  → later application
```

The paper found that immediate performance between Productive Failure and Direct Instruction could look similar, but Productive Failure showed stronger delayed retention in the tested setup. It also measured cognitive-load signals through heart-rate variability and found promising signs that students in the Productive Failure condition experienced a larger reduction in cognitive load after instruction.

### 3.2 BAG Learning Relevance

The BAG Learning research context identifies a South African higher-education problem shaped by:

- high-stakes exams
- crowded lecture environments
- fragmented notes and materials
- exam panic and cramming
- unequal access to private tutoring
- cognitive overload
- language barriers
- need for active retrieval and structured learning

Productive Failure Study Mode fits this context because it does not merely summarize notes. It creates a study interaction where the student must reveal what they understand, what they misunderstand, and where instruction should target next.

---

## 4. Product Thesis

The system should not behave like this:

```text
Student asks question
  → AI explains
  → student reads
  → student feels like they understand
```

It should behave like this:

```text
Student selects concept
  → AI asks a short pre-instruction challenge
  → student attempts
  → AI analyses the attempt
  → AI identifies the failure pattern
  → AI gives targeted consolidation
  → AI asks retrieval questions
  → student receives a next-step recommendation
```

The product should reward learning behaviour, not passive answer consumption.

---

## 5. Target Users

Primary user:

- South African university student preparing for tests, assignments, tutorials, or exams.

Initial demo user segments:

1. Law student learning offer and acceptance.
2. Commerce student learning break-even analysis or elasticity.
3. Engineering/science student learning forces, moments, or circuits.
4. Programming student learning Python lists, used as the paper-aligned case.

The demo must make it obvious that this is for **all university students**, not only computer science students.

---

## 6. User Problem

Students often study by:

- rereading notes
- highlighting slides
- asking AI for summaries
- asking AI for direct explanations
- cramming before exams
- avoiding hard practice until too late

This creates a dangerous illusion of understanding.

The product should solve this by making the student generate evidence of understanding before receiving the explanation.

---

## 7. User Story

As a South African university student, I want to study a difficult concept by first trying a short challenge, so that I can see what I actually understand before the AI explains it to me.

After I submit my attempt, I want the system to:

- identify what I got right
- identify what I misunderstood
- explain the missing concept clearly
- give me a worked example
- test me again with retrieval questions
- recommend what to revise next

---

## 8. Product Name Options

Preferred external/product name:

- **Attempt First Mode**

Preferred technical/project name:

- **PF-Zazi: Productive Failure Study Mode**

Reason:

- “Productive Failure” is useful for research and internal framing.
- “Attempt First Mode” is clearer for students.

---

## 9. Scope

### 9.1 In Scope

Build a full-stack prototype with:

- Next.js frontend
- React components
- TypeScript
- Tailwind CSS
- FastAPI backend
- Pydantic v2 schemas
- Supabase/Postgres persistence if time allows
- local fallback persistence if Supabase blocks delivery
- mock AI mode that works without API keys
- optional live AI mode behind environment variables
- structured Productive Failure flow
- discipline-agnostic concept model
- fixed demo concepts
- learning event dashboard
- eval harness
- README
- research mapping note
- demo script
- GitHub repository

### 9.2 Out of Scope

Do not build:

- full BAG Learning clone
- full Zazi clone
- real authentication
- payment system
- full document upload pipeline
- full RAG ingestion
- LMS integration
- production analytics
- real cognitive-load measurement
- multilingual translation in v1
- institutional admin portal
- browser extension
- mobile app
- cheating or assignment-completion tool

---

## 10. Non-Negotiable Product Requirements

The system must:

1. Force an attempt before the full explanation is shown.
2. Work across multiple disciplines.
3. Store the learning event.
4. Return structured failure analysis.
5. Generate targeted consolidation.
6. Generate a retrieval quiz.
7. Show a dashboard of learning behaviour.
8. Use typed backend contracts.
9. Include eval cases.
10. Run locally from README instructions.

The system must not:

1. Give the answer before the attempt.
2. Pretend to prove real learning outcomes from a prototype.
3. Store real student personal data.
4. Commit secrets.
5. Depend on a paid AI key to demo.
6. Use vague unvalidated model outputs at application boundaries.

---

## 11. Functional Requirements

### FR1: Concept Selection

The student must be able to select a concept from a seeded concept library.

Each concept must include:

- concept ID
- title
- discipline
- module context
- learning outcome
- prerequisite knowledge
- challenge type
- challenge prompt
- expected reasoning steps
- common misconceptions
- canonical explanation
- retrieval question seeds

Required seeded concepts:

1. Python lists — programming / computer science.
2. Offer and acceptance — law.
3. Break-even analysis or elasticity — commerce/economics.
4. Moments or forces — engineering/science.

### FR2: Pre-Instruction Challenge

After selecting a concept, the student receives a short challenge before any full explanation.

Challenge requirements:

- clear enough to attempt
- does not reveal the answer
- targets the concept directly
- supports partial answers
- encourages reasoning
- can be answered in free text

Challenge types:

- scenario_analysis
- calculation_attempt
- concept_explanation
- case_application
- compare_and_contrast
- diagnose_error
- short_problem_solving

### FR3: Student Attempt

The student submits:

- attempt text
- confidence score from 1 to 5
- optional confusion note

The UI must make the student feel safe to be wrong.

### FR4: Failure Analysis

The backend analyses the student attempt and returns structured failure analysis.

Required fields:

- failure label
- prior knowledge detected
- missing concept
- misconception summary
- productive failure score
- feedback strategy
- whether consolidation should proceed

Failure labels must be enum values.

Required failure label enum:

```text
missing_core_concept
misapplied_rule_or_formula
wrong_representation
unsupported_guess
surface_level_answer
partial_prior_knowledge
confuses_similar_concepts
calculation_without_reasoning
correct_but_incomplete
strong_attempt
```

### FR5: Targeted Consolidation

The system generates a consolidation response based on the failure analysis.

The consolidation must include:

- acknowledgement of the attempt
- what the student got right
- what was missing or confused
- short targeted explanation
- worked example
- one immediate retrieval prompt

The consolidation must be supportive, precise, and learning-oriented.

### FR6: Retrieval Quiz

The system generates a short retrieval quiz.

Quiz requirements:

- 3 questions
- at least 1 transfer question
- answer key hidden until submission
- feedback after submission
- mastery estimate
- recommended next step

### FR7: Dashboard

The dashboard must show:

- total sessions
- completed sessions
- average confidence score
- average quiz score
- failure label distribution
- recent learning events
- concepts attempted

This does not need to be production analytics. It must prove the data model and product loop.

---

## 12. AI Engineering Requirements

### 12.1 Schema-First Outputs

All AI-shaped responses must be parsed into Pydantic v2 models.

Do not pass raw AI dictionaries through the application.

Required AI output models:

- FailureAnalysis
- ConsolidationResponse
- RetrievalQuiz
- QuizResultFeedback

### 12.2 Mock AI Mode

The system must support mock AI mode.

Mock mode must:

- require no API key
- return deterministic structured responses
- support all demo concepts
- allow eval harness to run reliably
- allow the demo to work offline/local

### 12.3 Optional Live AI Mode

Live AI mode is optional.

If implemented, it must:

- use environment variables
- never commit API keys
- validate outputs through Pydantic
- fall back gracefully if the model fails
- avoid logging raw secrets
- include timeout and error handling

### 12.4 AI Safety and Academic Integrity

The AI must:

- avoid giving full assignment answers before an attempt
- avoid pretending unsupported content is certain
- avoid shaming students
- avoid exposing answer keys before quiz submission
- frame outputs as learning support
- refuse or redirect direct cheating-style requests

---

## 13. Data Model

### 13.1 Concept

Fields:

- concept_id: string
- title: string
- discipline: string
- module_context: string
- learning_outcome: string
- prerequisite_knowledge: list[string]
- challenge_type: enum
- challenge_prompt: string
- expected_reasoning_steps: list[string]
- common_misconceptions: list[string]
- canonical_explanation: string
- retrieval_question_seeds: list[string]

### 13.2 LearningSession

Fields:

- session_id: string
- concept_id: string
- student_alias: string | null
- status: enum
- created_at: datetime
- updated_at: datetime

Status enum:

```text
created
attempt_submitted
consolidated
quiz_completed
abandoned
```

### 13.3 StudentAttempt

Fields:

- attempt_id: string
- session_id: string
- attempt_text: string
- confidence_score: int
- confusion_note: string | null
- created_at: datetime

### 13.4 FailureAnalysis

Fields:

- analysis_id: string
- attempt_id: string
- failure_label: enum
- prior_knowledge_detected: list[string]
- missing_concept: string
- misconception_summary: string
- productive_failure_score: int
- feedback_strategy: string
- should_consolidate: bool
- created_at: datetime

Productive failure score:

- 1 = no meaningful attempt
- 2 = weak attempt, little usable reasoning
- 3 = partial reasoning, useful failure
- 4 = strong attempt with specific gap
- 5 = near-correct or strong reasoning

### 13.5 ConsolidationResponse

Fields:

- response_id: string
- analysis_id: string
- acknowledgement: string
- what_was_useful: list[string]
- missing_or_confused: list[string]
- explanation: string
- worked_example: string
- immediate_retrieval_prompt: string
- created_at: datetime

### 13.6 RetrievalQuiz

Fields:

- quiz_id: string
- session_id: string
- questions: list[QuizQuestion]
- answer_key: list[QuizAnswer]
- created_at: datetime

### 13.7 QuizQuestion

Fields:

- question_id: string
- question_text: string
- question_type: enum
- options: list[string] | null

Question type enum:

```text
short_answer
multiple_choice
scenario_transfer
calculation
```

### 13.8 QuizResult

Fields:

- result_id: string
- quiz_id: string
- session_id: string
- score: float
- feedback: list[string]
- mastery_estimate: enum
- recommended_next_step: string
- created_at: datetime

Mastery estimate enum:

```text
needs_review
developing
almost_there
secure
```

---

## 14. API Requirements

Backend framework: FastAPI.

### GET /health

Returns service health.

Response:

```json
{
  "status": "ok",
  "service": "productive-failure-api"
}
```

### GET /concepts

Returns seeded concepts.

### GET /concepts/{concept_id}

Returns one concept.

### POST /sessions

Creates a learning session.

Request:

```json
{
  "concept_id": "law_offer_acceptance",
  "student_alias": "demo-student"
}
```

Response:

```json
{
  "session_id": "...",
  "concept": {},
  "challenge": {}
}
```

### POST /sessions/{session_id}/attempt

Submits a student attempt and returns failure analysis, consolidation, and quiz.

Request:

```json
{
  "attempt_text": "I think acceptance happens when both people agree somehow.",
  "confidence_score": 2,
  "confusion_note": "I am not sure when acceptance becomes legally valid."
}
```

Response:

```json
{
  "attempt_id": "...",
  "failure_analysis": {},
  "consolidation": {},
  "retrieval_quiz": {}
}
```

### POST /sessions/{session_id}/quiz

Submits quiz answers.

Request:

```json
{
  "answers": [
    {"question_id": "q1", "answer_text": "..."},
    {"question_id": "q2", "answer_text": "..."},
    {"question_id": "q3", "answer_text": "..."}
  ]
}
```

Response:

```json
{
  "quiz_result": {},
  "recommended_next_step": "..."
}
```

### GET /sessions/{session_id}

Returns full learning session trace.

### GET /dashboard

Returns aggregate dashboard metrics.

---

## 15. Frontend Requirements

Frontend framework: Next.js + React + TypeScript + Tailwind.

### 15.1 Required Pages

#### `/`

Home page.

Must explain:

- Attempt First Mode
- why the student attempts before explanation
- start button

#### `/learn`

Concept selection page.

Must show concept cards:

- title
- discipline
- learning goal
- challenge type

#### `/session/[id]`

Main learning flow page.

Must show:

1. selected concept
2. pre-instruction challenge
3. attempt textbox
4. confidence selector
5. failure analysis card
6. consolidation card
7. retrieval quiz
8. quiz result

#### `/dashboard`

Learning event dashboard.

Must show:

- metrics cards
- failure label distribution
- recent sessions

#### `/about`

Project explanation page.

Must include:

- research basis
- product hypothesis
- stack
- limitations
- next steps

### 15.2 UI Quality Bar

The UI should be clean and credible.

Avoid:

- clutter
- neon toy styling
- fake analytics overload
- irrelevant animations

Prefer:

- clear hierarchy
- readable cards
- strong empty states
- simple learning-flow progression
- BAG-adjacent education-product feel

---

## 16. Persistence Requirements

Preferred persistence:

- Supabase Postgres.

Fallback persistence:

- SQLite or JSON file repository.

Persistence must be behind an adapter boundary.

Do not hardcode database logic inside route handlers.

Suggested interface:

```text
LearningRepository
  - list_concepts()
  - get_concept(concept_id)
  - create_session(...)
  - save_attempt(...)
  - save_failure_analysis(...)
  - save_consolidation(...)
  - save_quiz(...)
  - save_quiz_result(...)
  - get_session_trace(session_id)
  - get_dashboard_metrics()
```

---

## 17. Eval Harness Requirements

The project must include a small eval harness.

Purpose:

- prove the AI behaviour is structured
- catch obvious regressions
- show serious AI engineering judgment
- demonstrate that the feature can be evaluated later with real student data

### 17.1 Minimum Eval Cases

1. Law attempt: vague offer and acceptance answer.
2. Law attempt: strong but incomplete offer and acceptance answer.
3. Commerce attempt: calculation without reasoning.
4. Commerce attempt: wrong formula application.
5. Engineering/science attempt: surface-level explanation.
6. Python lists attempt: wrong representation.
7. Python lists attempt: near-correct answer.
8. Student tries to skip attempt and asks for answer.
9. Unsupported nonsense answer.
10. Correct answer that still requires transfer quiz.

### 17.2 Eval Checks

Each case must check:

- valid schema returned
- expected failure label or acceptable label set
- consolidation exists
- feedback is relevant to the failure label
- quiz has 3 questions
- at least 1 transfer question exists
- answer key is not exposed before quiz submission
- no direct full answer is given before attempt

### 17.3 Eval Output

Eval runner must output:

- case ID
- pass/fail
- failure reason
- expected label
- actual label
- summary pass rate

---

## 18. Testing Requirements

Backend tests:

- health endpoint
- concepts endpoint
- create session
- submit attempt
- quiz submission
- dashboard metrics
- Pydantic validation for failure labels
- mock AI deterministic response

Frontend tests are optional because of time.

Minimum validation gate:

- backend tests pass
- frontend builds
- eval harness runs

---

## 19. Privacy and Compliance Requirements

This is a demo prototype, but it should model sane privacy behaviour.

Requirements:

- use demo concepts only
- do not use real student data
- do not upload copyrighted university material
- use aliases, not real names
- do not commit secrets
- do not log API keys
- do not claim POPIA compliance
- include POPIA-aligned notes: minimization, deletion, consent, and data boundaries

---

## 20. Academic Integrity Requirements

The product must be framed as learning support.

It must not be framed as:

- assignment completion
- essay writing automation
- exam answer generation
- cheating helper

The UI and docs should say:

> This mode is designed to help students learn by attempting first, receiving feedback, and practising retrieval. It is not designed to complete assessed work for students.

---

## 21. Repo Structure

Recommended simple repo structure:

```text
productive-failure-study-mode/
  frontend/
    app/
    components/
    lib/
    package.json
  backend/
    app/
      main.py
      models.py
      routes.py
      settings.py
      services/
      repositories/
      evals/
    tests/
    pyproject.toml
    .env.example
  docs/
    PRD.md
    RESEARCH_MAPPING.md
    ARCHITECTURE.md
    DEMO_SCRIPT.md
  README.md
  .gitignore
```

Do not use an overcomplicated monorepo if it slows delivery.

---

## 22. Build Phases and Gates

### Phase 0: Project Contract and Repo Setup

Deliverables:

- GitHub repo initialized
- README skeleton
- `/docs/PRD.md` added
- `.gitignore`
- `.env.example`
- frontend and backend folders created

Gate:

- repo exists
- first commit pushed
- README states the north star clearly
- project can be opened cleanly in VS Code

### Phase 1: Backend Contracts

Deliverables:

- FastAPI app
- Pydantic models
- health endpoint
- concepts endpoint
- seeded concepts
- pytest setup

Gate:

- backend starts locally
- `/health` returns OK
- `/concepts` returns typed seeded concepts
- backend tests pass

### Phase 2: Core Productive Failure Flow

Deliverables:

- create session endpoint
- submit attempt endpoint
- mock failure analysis service
- mock consolidation service
- mock retrieval quiz service
- session trace endpoint

Gate:

- one complete learning session works through API
- all AI-shaped outputs validate through Pydantic
- failure labels are enums
- no raw dict-passing at model boundaries

### Phase 3: Persistence

Deliverables:

- repository interface
- persistence adapter
- Supabase/Postgres if time allows
- local fallback if needed
- dashboard metrics endpoint

Gate:

- sessions persist
- dashboard metrics update after a completed session
- route handlers do not directly own database logic
- fallback mode works if Supabase is unavailable

### Phase 4: Frontend Learning Flow

Deliverables:

- Next.js app
- home page
- concept selection page
- session page
- dashboard page
- API client

Gate:

- user can complete one full session from the browser
- failure analysis appears after attempt
- consolidation appears after analysis
- quiz can be submitted
- dashboard updates

### Phase 5: Eval Harness

Deliverables:

- fixed eval cases
- eval runner
- expected labels
- pass/fail report
- regression notes

Gate:

- eval runner executes locally
- at least 8 eval cases exist
- failures have readable reasons
- mock AI mode passes baseline cases

### Phase 6: Documentation and Demo Packaging

Deliverables:

- polished README
- research mapping note
- architecture note
- demo script
- screenshots if possible
- limitations section
- next steps section

Gate:

- reviewer can understand the project in 3 minutes
- developer can run it from README
- demo can be shown in under 5 minutes
- docs do not overclaim real student learning outcomes

### Phase 7: Optional Hosting

Deliverables:

- frontend deployed if safe
- backend deployed if safe
- environment variables configured safely

Gate:

- hosted demo works end-to-end

Important rule:

If hosting threatens code quality, skip hosting. A clean local demo plus GitHub repo is better than a broken deployment.

---

## 23. 12-Hour Build Priority

Priority order:

1. Working full learning flow.
2. Typed FastAPI/Pydantic contracts.
3. Clean Next.js UI.
4. Mock AI mode.
5. Persistence and dashboard.
6. Eval harness.
7. README and demo script.
8. Hosting only if everything else is stable.

Cut aggressively if needed.

Do not sacrifice the core learning flow for polish.

---

## 24. Demo Script

The final demo should run in under 5 minutes.

Suggested demo sequence:

1. Open README.
2. State the north star.
3. Start backend.
4. Start frontend.
5. Open the app.
6. Select “Law: Offer and Acceptance.”
7. Submit an imperfect attempt.
8. Show failure analysis.
9. Show targeted consolidation.
10. Complete retrieval quiz.
11. Show dashboard update.
12. Briefly open code:
    - Pydantic schemas
    - FastAPI route
    - mock AI service
    - eval cases
13. Explain next steps inside BAG Learning:
    - connect to uploaded course materials
    - ground challenges in retrieved syllabus chunks
    - add spaced follow-ups
    - add institution-level analytics
    - run real learning-outcome evals

---

## 25. Final Success Definition

This project succeeds if a reviewer at BAG Learning can see that the builder:

- understands the student problem
- understands BAG Learning's likely product direction
- can apply research without being academic or vague
- can build in their stack
- can use AI safely and structurally
- can write typed backend contracts
- can create a usable frontend
- can think about evals and learning outcomes
- can work like a developer, not just an intern

The desired reaction:

> This person may be underqualified on paper, but they think like a product engineer and can build.

---

## 26. Non-Claims

Do not claim:

- this proves Productive Failure improves BAG Learning outcomes
- this is production-ready
- this is POPIA compliant
- this replaces Zazi
- this works for every subject without further validation
- this has been tested with real students

Correct claim:

> This is a production-shaped feature spike showing how Productive Failure could be operationalized inside a BAG Learning-style AI study companion, with typed contracts, mock AI, persistence, dashboard metrics, and an eval harness.

---

## 27. Instructions for the LLM Builder

When using this PRD with another LLM, instruct it to behave like a staff-level product engineer.

The LLM must:

- ask for missing repo state before editing existing code
- use PowerShell-compatible commands
- prefer full files over vague patches
- keep setup, validation, and git commands separate
- avoid overbuilding
- preserve the north star
- implement one phase at a time
- enforce gates before moving to the next phase
- include tests before commit instructions
- never commit secrets
- never make unsupported production claims

For each phase, the LLM should output:

1. What will be built.
2. Files to create or modify.
3. Full file contents where needed.
4. PowerShell commands.
5. Validation/test commands.
6. Git commands only after validation.
7. Gate checklist.
8. Next phase recommendation.

