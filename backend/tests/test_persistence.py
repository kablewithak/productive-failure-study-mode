from __future__ import annotations

from pathlib import Path

from app.concept_seed import CONCEPTS_BY_ID
from app.models import QuizSubmittedAnswer, SessionStatus, StudentAttempt
from app.repositories.json_file import JsonFileLearningRepository
from app.services.mock_learning_engine import MockLearningEngine
from app.time_utils import utc_now


def test_json_repository_persists_full_learning_event_across_instances(tmp_path: Path) -> None:
    store_path = tmp_path / "learning_store.json"
    repository = JsonFileLearningRepository(store_path=store_path)
    concept = CONCEPTS_BY_ID["law_offer_acceptance"]
    session = repository.create_session(concept_id=concept.concept_id, student_alias="demo-student")
    attempt = StudentAttempt(
        attempt_id="attempt-1",
        session_id=session.session_id,
        attempt_text="This is not acceptance because the reply changes the offer terms.",
        confidence_score=4,
        confusion_note=None,
        created_at=utc_now(),
    )
    engine = MockLearningEngine()
    analysis, consolidation, quiz = engine.build_attempt_outputs(concept=concept, attempt=attempt)

    repository.save_attempt_bundle(
        session_id=session.session_id,
        attempt=attempt,
        failure_analysis=analysis,
        consolidation=consolidation,
        retrieval_quiz=quiz,
    )
    result = engine.score_quiz(
        quiz=quiz,
        submitted_answers=[
            QuizSubmittedAnswer(question_id="q1", answer_text="Acceptance must match the offer."),
            QuizSubmittedAnswer(question_id="q2", answer_text="Changing material terms matters."),
            QuizSubmittedAnswer(question_id="q3", answer_text="Apply the rule to the new facts."),
        ],
    )
    repository.save_quiz_result(session_id=session.session_id, quiz_result=result)

    reloaded_repository = JsonFileLearningRepository(store_path=store_path)
    reloaded_session = reloaded_repository.get_session(session.session_id)

    assert reloaded_session is not None
    assert reloaded_session.status == SessionStatus.QUIZ_COMPLETED
    assert reloaded_repository.get_attempt(session.session_id) == attempt
    assert reloaded_repository.get_failure_analysis(session.session_id) == analysis
    assert reloaded_repository.get_consolidation(session.session_id) == consolidation
    assert reloaded_repository.get_quiz(session.session_id) == quiz
    assert reloaded_repository.get_quiz_result(session.session_id) == result


def test_json_repository_lists_sessions_newest_first(tmp_path: Path) -> None:
    repository = JsonFileLearningRepository(store_path=tmp_path / "learning_store.json")
    first = repository.create_session(concept_id="law_offer_acceptance", student_alias=None)
    second = repository.create_session(concept_id="commerce_break_even_analysis", student_alias=None)

    listed_sessions = repository.list_sessions()

    assert [session.session_id for session in listed_sessions] == [second.session_id, first.session_id]
