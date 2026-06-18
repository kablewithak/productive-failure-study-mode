from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.models import (
    ConsolidationResponse,
    FailureAnalysis,
    LearningSession,
    QuizResultFeedback,
    SessionStatus,
    StudentAttempt,
    StoredRetrievalQuiz,
)


def utc_now() -> datetime:
    return datetime.now(UTC)


class InMemoryLearningRepository:
    """Small local repository for Phase 2 API behaviour.

    This is intentionally not durable persistence. It lets the API expose a real
    session trace while keeping the durable storage decision behind a later
    repository adapter boundary.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, LearningSession] = {}
        self._attempts_by_session_id: dict[str, StudentAttempt] = {}
        self._analyses_by_session_id: dict[str, FailureAnalysis] = {}
        self._consolidations_by_session_id: dict[str, ConsolidationResponse] = {}
        self._quizzes_by_session_id: dict[str, StoredRetrievalQuiz] = {}
        self._quiz_results_by_session_id: dict[str, QuizResultFeedback] = {}

    def create_session(self, concept_id: str, student_alias: str | None) -> LearningSession:
        now = utc_now()
        session = LearningSession(
            session_id=str(uuid4()),
            concept_id=concept_id,
            student_alias=student_alias,
            status=SessionStatus.CREATED,
            created_at=now,
            updated_at=now,
        )
        self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> LearningSession | None:
        return self._sessions.get(session_id)

    def save_attempt_bundle(
        self,
        session_id: str,
        attempt: StudentAttempt,
        failure_analysis: FailureAnalysis,
        consolidation: ConsolidationResponse,
        retrieval_quiz: StoredRetrievalQuiz,
    ) -> None:
        self._attempts_by_session_id[session_id] = attempt
        self._analyses_by_session_id[session_id] = failure_analysis
        self._consolidations_by_session_id[session_id] = consolidation
        self._quizzes_by_session_id[session_id] = retrieval_quiz
        self._set_status(session_id=session_id, status=SessionStatus.CONSOLIDATED)

    def save_quiz_result(self, session_id: str, quiz_result: QuizResultFeedback) -> None:
        self._quiz_results_by_session_id[session_id] = quiz_result
        self._set_status(session_id=session_id, status=SessionStatus.QUIZ_COMPLETED)

    def get_attempt(self, session_id: str) -> StudentAttempt | None:
        return self._attempts_by_session_id.get(session_id)

    def get_failure_analysis(self, session_id: str) -> FailureAnalysis | None:
        return self._analyses_by_session_id.get(session_id)

    def get_consolidation(self, session_id: str) -> ConsolidationResponse | None:
        return self._consolidations_by_session_id.get(session_id)

    def get_quiz(self, session_id: str) -> StoredRetrievalQuiz | None:
        return self._quizzes_by_session_id.get(session_id)

    def get_quiz_result(self, session_id: str) -> QuizResultFeedback | None:
        return self._quiz_results_by_session_id.get(session_id)

    def _set_status(self, session_id: str, status: SessionStatus) -> None:
        session = self._sessions[session_id]
        self._sessions[session_id] = session.model_copy(
            update={"status": status, "updated_at": utc_now()}
        )
