from __future__ import annotations

from collections import Counter
from statistics import mean
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.concept_seed import CONCEPTS_BY_ID, SEEDED_CONCEPTS
from app.models import (
    ApiError,
    ChallengePreview,
    Concept,
    ConceptAttemptSummary,
    ConceptListResponse,
    ConceptResponse,
    ConceptSummary,
    CreateSessionRequest,
    CreateSessionResponse,
    DashboardMetricsResponse,
    FailureLabelDistributionItem,
    HealthResponse,
    RecentLearningEvent,
    RetrievalQuiz,
    SessionStatus,
    SessionTraceResponse,
    StudentAttempt,
    SubmitAttemptRequest,
    SubmitAttemptResponse,
    SubmitQuizRequest,
    SubmitQuizResponse,
)
from app.repositories.base import LearningRepository
from app.repositories.json_file import JsonFileLearningRepository
from app.repositories.memory import InMemoryLearningRepository
from app.services.mock_learning_engine import MockLearningEngine
from app.settings import AppSettings, load_settings
from app.time_utils import utc_now


settings = load_settings()


def _build_repository(app_settings: AppSettings) -> LearningRepository:
    if app_settings.storage_mode == "memory":
        return InMemoryLearningRepository()
    if app_settings.storage_mode in {"local", "local_json"}:
        return JsonFileLearningRepository(store_path=app_settings.local_store_path)
    raise ValueError(f"Unsupported PF_STORAGE_MODE: {app_settings.storage_mode!r}.")


app = FastAPI(
    title="Productive Failure Study Mode API",
    description=(
        "Backend contract for an Attempt First Mode learning flow: concept selection, "
        "pre-instruction challenge, typed failure analysis, consolidation, retrieval quiz, "
        "and learning-event dashboard."
    ),
    version="0.4.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["content-type"],
)

repository: LearningRepository = _build_repository(settings)
learning_engine = MockLearningEngine()


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="productive-failure-api")


@app.get("/concepts", response_model=ConceptListResponse)
def list_concepts() -> ConceptListResponse:
    return ConceptListResponse(concepts=list(SEEDED_CONCEPTS))


@app.get(
    "/concepts/{concept_id}",
    response_model=ConceptResponse,
    responses={404: {"model": ApiError}},
)
def get_concept(concept_id: str) -> ConceptResponse:
    return ConceptResponse(concept=_get_concept_or_404(concept_id))


@app.post(
    "/sessions",
    response_model=CreateSessionResponse,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"model": ApiError}},
)
def create_session(request: CreateSessionRequest) -> CreateSessionResponse:
    concept = _get_concept_or_404(request.concept_id)
    session = repository.create_session(
        concept_id=concept.concept_id,
        student_alias=request.student_alias,
    )
    return CreateSessionResponse(
        session_id=session.session_id,
        concept=_concept_summary(concept),
        challenge=_challenge_preview(concept),
    )


@app.post(
    "/sessions/{session_id}/attempt",
    response_model=SubmitAttemptResponse,
    responses={404: {"model": ApiError}},
)
def submit_attempt(session_id: str, request: SubmitAttemptRequest) -> SubmitAttemptResponse:
    session = _get_session_or_404(session_id)
    concept = _get_concept_or_404(session.concept_id)

    attempt = StudentAttempt(
        attempt_id=str(uuid4()),
        session_id=session.session_id,
        attempt_text=request.attempt_text,
        confidence_score=request.confidence_score,
        confusion_note=request.confusion_note,
        created_at=utc_now(),
    )
    failure_analysis, consolidation, stored_quiz = learning_engine.build_attempt_outputs(
        concept=concept,
        attempt=attempt,
    )
    repository.save_attempt_bundle(
        session_id=session.session_id,
        attempt=attempt,
        failure_analysis=failure_analysis,
        consolidation=consolidation,
        retrieval_quiz=stored_quiz,
    )
    return SubmitAttemptResponse(
        attempt_id=attempt.attempt_id,
        failure_analysis=failure_analysis,
        consolidation=consolidation,
        retrieval_quiz=_public_quiz(stored_quiz),
    )


@app.post(
    "/sessions/{session_id}/quiz",
    response_model=SubmitQuizResponse,
    responses={404: {"model": ApiError}, 409: {"model": ApiError}},
)
def submit_quiz(session_id: str, request: SubmitQuizRequest) -> SubmitQuizResponse:
    _get_session_or_404(session_id)
    quiz = repository.get_quiz(session_id)
    if quiz is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error_code": "quiz_not_ready",
                "message": "Submit an attempt before submitting quiz answers.",
            },
        )

    quiz_result = learning_engine.score_quiz(quiz=quiz, submitted_answers=request.answers)
    repository.save_quiz_result(session_id=session_id, quiz_result=quiz_result)
    return SubmitQuizResponse(
        quiz_result=quiz_result,
        recommended_next_step=quiz_result.recommended_next_step,
    )


@app.get(
    "/sessions/{session_id}",
    response_model=SessionTraceResponse,
    responses={404: {"model": ApiError}},
)
def get_session_trace(session_id: str) -> SessionTraceResponse:
    session = _get_session_or_404(session_id)
    concept = _get_concept_or_404(session.concept_id)
    stored_quiz = repository.get_quiz(session_id)
    return SessionTraceResponse(
        session=session,
        concept=_concept_summary(concept),
        challenge=_challenge_preview(concept),
        attempt=repository.get_attempt(session_id),
        failure_analysis=repository.get_failure_analysis(session_id),
        consolidation=repository.get_consolidation(session_id),
        retrieval_quiz=_public_quiz(stored_quiz) if stored_quiz else None,
        quiz_result=repository.get_quiz_result(session_id),
    )


@app.get("/dashboard", response_model=DashboardMetricsResponse)
def get_dashboard() -> DashboardMetricsResponse:
    sessions = repository.list_sessions()
    attempts = [
        attempt
        for session in sessions
        if (attempt := repository.get_attempt(session.session_id)) is not None
    ]
    analyses = [
        analysis
        for session in sessions
        if (analysis := repository.get_failure_analysis(session.session_id)) is not None
    ]
    quiz_results = [
        quiz_result
        for session in sessions
        if (quiz_result := repository.get_quiz_result(session.session_id)) is not None
    ]

    failure_counts = Counter(analysis.failure_label for analysis in analyses)
    concept_attempt_counts = Counter(
        session.concept_id
        for session in sessions
        if repository.get_attempt(session.session_id) is not None
    )

    return DashboardMetricsResponse(
        total_sessions=len(sessions),
        completed_sessions=sum(1 for session in sessions if session.status == SessionStatus.QUIZ_COMPLETED),
        average_confidence_score=_average_or_none([attempt.confidence_score for attempt in attempts]),
        average_quiz_score=_average_or_none([quiz_result.score for quiz_result in quiz_results]),
        failure_label_distribution=[
            FailureLabelDistributionItem(failure_label=label, count=count)
            for label, count in sorted(failure_counts.items(), key=lambda item: item[0].value)
        ],
        recent_learning_events=_recent_learning_events(sessions),
        concepts_attempted=_concepts_attempted(concept_attempt_counts),
    )



def _get_concept_or_404(concept_id: str) -> Concept:
    concept = CONCEPTS_BY_ID.get(concept_id)
    if concept is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "concept_not_found",
                "message": f"No seeded concept exists for concept_id '{concept_id}'.",
            },
        )
    return concept


def _get_session_or_404(session_id: str):
    session = repository.get_session(session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "session_not_found",
                "message": f"No learning session exists for session_id '{session_id}'.",
            },
        )
    return session


def _concept_summary(concept: Concept) -> ConceptSummary:
    return ConceptSummary(
        concept_id=concept.concept_id,
        title=concept.title,
        discipline=concept.discipline,
        module_context=concept.module_context,
        learning_outcome=concept.learning_outcome,
        challenge_type=concept.challenge_type,
    )


def _challenge_preview(concept: Concept) -> ChallengePreview:
    return ChallengePreview(
        concept_id=concept.concept_id,
        challenge_type=concept.challenge_type,
        challenge_prompt=concept.challenge_prompt,
    )


def _public_quiz(stored_quiz) -> RetrievalQuiz:
    return RetrievalQuiz(
        quiz_id=stored_quiz.quiz_id,
        session_id=stored_quiz.session_id,
        questions=stored_quiz.questions,
        created_at=stored_quiz.created_at,
    )


def _average_or_none(values: list[float | int]) -> float | None:
    if not values:
        return None
    return round(float(mean(values)), 3)


def _recent_learning_events(sessions) -> list[RecentLearningEvent]:
    events: list[RecentLearningEvent] = []
    for session in sessions[:10]:
        concept = _get_concept_or_404(session.concept_id)
        attempt = repository.get_attempt(session.session_id)
        analysis = repository.get_failure_analysis(session.session_id)
        quiz_result = repository.get_quiz_result(session.session_id)
        events.append(
            RecentLearningEvent(
                session_id=session.session_id,
                concept_id=concept.concept_id,
                concept_title=concept.title,
                discipline=concept.discipline,
                status=session.status,
                failure_label=analysis.failure_label if analysis else None,
                confidence_score=attempt.confidence_score if attempt else None,
                quiz_score=quiz_result.score if quiz_result else None,
                created_at=session.created_at,
                updated_at=session.updated_at,
            )
        )
    return events


def _concepts_attempted(concept_attempt_counts: Counter[str]) -> list[ConceptAttemptSummary]:
    summaries: list[ConceptAttemptSummary] = []
    for concept_id, attempt_count in sorted(concept_attempt_counts.items()):
        concept = _get_concept_or_404(concept_id)
        summaries.append(
            ConceptAttemptSummary(
                concept_id=concept.concept_id,
                title=concept.title,
                discipline=concept.discipline,
                attempt_count=attempt_count,
            )
        )
    return summaries
