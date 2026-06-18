from __future__ import annotations

from typing import Protocol

from app.models import (
    ConsolidationResponse,
    FailureAnalysis,
    LearningSession,
    QuizResultFeedback,
    StudentAttempt,
    StoredRetrievalQuiz,
)


class LearningRepository(Protocol):
    """Persistence seam for the Attempt First learning flow.

    Implementations may be in-memory, local JSON, or later Postgres/Supabase.
    Route handlers should depend on this contract rather than storage details.
    """

    def create_session(self, concept_id: str, student_alias: str | None) -> LearningSession:
        ...

    def get_session(self, session_id: str) -> LearningSession | None:
        ...

    def list_sessions(self) -> list[LearningSession]:
        ...

    def save_attempt_bundle(
        self,
        session_id: str,
        attempt: StudentAttempt,
        failure_analysis: FailureAnalysis,
        consolidation: ConsolidationResponse,
        retrieval_quiz: StoredRetrievalQuiz,
    ) -> None:
        ...

    def save_quiz_result(self, session_id: str, quiz_result: QuizResultFeedback) -> None:
        ...

    def get_attempt(self, session_id: str) -> StudentAttempt | None:
        ...

    def get_failure_analysis(self, session_id: str) -> FailureAnalysis | None:
        ...

    def get_consolidation(self, session_id: str) -> ConsolidationResponse | None:
        ...

    def get_quiz(self, session_id: str) -> StoredRetrievalQuiz | None:
        ...

    def get_quiz_result(self, session_id: str) -> QuizResultFeedback | None:
        ...
