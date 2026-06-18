from __future__ import annotations

import json
import os
from pathlib import Path
from threading import RLock
from typing import Any
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
from app.time_utils import utc_now


class JsonFileLearningRepository:
    """Durable local repository for the Phase 3 prototype.

    This is the local fallback persistence adapter. It deliberately keeps all
    storage-specific JSON mechanics behind the repository seam so route handlers
    do not learn about file paths, serialization, or atomic writes.
    """

    _VERSION = 1

    def __init__(self, store_path: Path) -> None:
        self._store_path = store_path
        self._lock = RLock()
        self._sessions: dict[str, LearningSession] = {}
        self._attempts_by_session_id: dict[str, StudentAttempt] = {}
        self._analyses_by_session_id: dict[str, FailureAnalysis] = {}
        self._consolidations_by_session_id: dict[str, ConsolidationResponse] = {}
        self._quizzes_by_session_id: dict[str, StoredRetrievalQuiz] = {}
        self._quiz_results_by_session_id: dict[str, QuizResultFeedback] = {}
        self._load()

    def create_session(self, concept_id: str, student_alias: str | None) -> LearningSession:
        with self._lock:
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
            self._persist()
            return session

    def get_session(self, session_id: str) -> LearningSession | None:
        with self._lock:
            return self._sessions.get(session_id)

    def list_sessions(self) -> list[LearningSession]:
        with self._lock:
            return sorted(
                self._sessions.values(),
                key=lambda session: session.updated_at,
                reverse=True,
            )

    def save_attempt_bundle(
        self,
        session_id: str,
        attempt: StudentAttempt,
        failure_analysis: FailureAnalysis,
        consolidation: ConsolidationResponse,
        retrieval_quiz: StoredRetrievalQuiz,
    ) -> None:
        with self._lock:
            self._attempts_by_session_id[session_id] = attempt
            self._analyses_by_session_id[session_id] = failure_analysis
            self._consolidations_by_session_id[session_id] = consolidation
            self._quizzes_by_session_id[session_id] = retrieval_quiz
            self._set_status(session_id=session_id, status=SessionStatus.CONSOLIDATED)
            self._persist()

    def save_quiz_result(self, session_id: str, quiz_result: QuizResultFeedback) -> None:
        with self._lock:
            self._quiz_results_by_session_id[session_id] = quiz_result
            self._set_status(session_id=session_id, status=SessionStatus.QUIZ_COMPLETED)
            self._persist()

    def get_attempt(self, session_id: str) -> StudentAttempt | None:
        with self._lock:
            return self._attempts_by_session_id.get(session_id)

    def get_failure_analysis(self, session_id: str) -> FailureAnalysis | None:
        with self._lock:
            return self._analyses_by_session_id.get(session_id)

    def get_consolidation(self, session_id: str) -> ConsolidationResponse | None:
        with self._lock:
            return self._consolidations_by_session_id.get(session_id)

    def get_quiz(self, session_id: str) -> StoredRetrievalQuiz | None:
        with self._lock:
            return self._quizzes_by_session_id.get(session_id)

    def get_quiz_result(self, session_id: str) -> QuizResultFeedback | None:
        with self._lock:
            return self._quiz_results_by_session_id.get(session_id)

    def _set_status(self, session_id: str, status: SessionStatus) -> None:
        session = self._sessions[session_id]
        self._sessions[session_id] = session.model_copy(
            update={"status": status, "updated_at": utc_now()}
        )

    def _load(self) -> None:
        if not self._store_path.exists():
            return

        raw_payload = json.loads(self._store_path.read_text(encoding="utf-8"))
        if raw_payload.get("version") != self._VERSION:
            raise ValueError(
                f"Unsupported learning store version: {raw_payload.get('version')!r}."
            )

        self._sessions = self._parse_mapping(raw_payload, "sessions", LearningSession)
        self._attempts_by_session_id = self._parse_mapping(
            raw_payload,
            "attempts_by_session_id",
            StudentAttempt,
        )
        self._analyses_by_session_id = self._parse_mapping(
            raw_payload,
            "analyses_by_session_id",
            FailureAnalysis,
        )
        self._consolidations_by_session_id = self._parse_mapping(
            raw_payload,
            "consolidations_by_session_id",
            ConsolidationResponse,
        )
        self._quizzes_by_session_id = self._parse_mapping(
            raw_payload,
            "quizzes_by_session_id",
            StoredRetrievalQuiz,
        )
        self._quiz_results_by_session_id = self._parse_mapping(
            raw_payload,
            "quiz_results_by_session_id",
            QuizResultFeedback,
        )

    def _persist(self) -> None:
        payload = {
            "version": self._VERSION,
            "sessions": self._dump_mapping(self._sessions),
            "attempts_by_session_id": self._dump_mapping(self._attempts_by_session_id),
            "analyses_by_session_id": self._dump_mapping(self._analyses_by_session_id),
            "consolidations_by_session_id": self._dump_mapping(self._consolidations_by_session_id),
            "quizzes_by_session_id": self._dump_mapping(self._quizzes_by_session_id),
            "quiz_results_by_session_id": self._dump_mapping(self._quiz_results_by_session_id),
        }

        self._store_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self._store_path.with_suffix(f"{self._store_path.suffix}.tmp")
        temp_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        os.replace(temp_path, self._store_path)

    def _parse_mapping(self, payload: dict[str, Any], key: str, model_type: Any) -> dict[str, Any]:
        raw_mapping = payload.get(key, {})
        if not isinstance(raw_mapping, dict):
            raise ValueError(f"Learning store key '{key}' must contain an object.")
        return {
            identifier: model_type.model_validate(raw_model)
            for identifier, raw_model in raw_mapping.items()
        }

    def _dump_mapping(self, mapping: dict[str, Any]) -> dict[str, Any]:
        return {
            identifier: model.model_dump(mode="json")
            for identifier, model in mapping.items()
        }
