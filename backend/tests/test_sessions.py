from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.models import FailureAnalysis, FailureLabel, RetrievalQuiz


client = TestClient(app)


def _create_law_session() -> str:
    response = client.post(
        "/sessions",
        json={"concept_id": "law_offer_acceptance", "student_alias": "demo-student"},
    )
    assert response.status_code == 201
    return response.json()["session_id"]


def test_create_session_returns_attempt_first_challenge_without_explanation_leakage() -> None:
    response = client.post(
        "/sessions",
        json={"concept_id": "law_offer_acceptance", "student_alias": "demo-student"},
    )

    assert response.status_code == 201
    payload = response.json()

    assert payload["session_id"]
    assert payload["concept"]["concept_id"] == "law_offer_acceptance"
    assert payload["challenge"]["challenge_type"] == "case_application"
    assert "canonical_explanation" not in payload["concept"]
    assert "canonical_explanation" not in payload["challenge"]


def test_create_session_rejects_unknown_concept() -> None:
    response = client.post(
        "/sessions",
        json={"concept_id": "not_a_real_concept", "student_alias": "demo-student"},
    )

    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "concept_not_found"


def test_submit_attempt_returns_typed_failure_analysis_consolidation_and_public_quiz() -> None:
    session_id = _create_law_session()

    response = client.post(
        f"/sessions/{session_id}/attempt",
        json={
            "attempt_text": "I think it is accepted because the buyer sounds like they agree, but I am not sure about the laptop bag.",
            "confidence_score": 2,
            "confusion_note": "I do not know when changed terms matter.",
        },
    )

    assert response.status_code == 200
    payload = response.json()

    analysis = FailureAnalysis.model_validate(payload["failure_analysis"])
    assert analysis.failure_label in {
        FailureLabel.PARTIAL_PRIOR_KNOWLEDGE,
        FailureLabel.STRONG_ATTEMPT,
    }
    assert analysis.should_consolidate is True
    assert payload["consolidation"]["explanation"]
    assert payload["failure_analysis"]["source"]["citation_label"].startswith("Sample")
    assert payload["failure_analysis"]["matched_rubric_items"]
    assert payload["failure_analysis"]["missing_rubric_items"]
    assert payload["consolidation"]["source"]["title"].startswith("Sample")

    quiz = RetrievalQuiz.model_validate(payload["retrieval_quiz"])
    assert len(quiz.questions) == 3
    assert any(question.question_type == "scenario_transfer" for question in quiz.questions)
    assert quiz.source.citation_label.startswith("Sample")
    assert all(question.source_citation_label for question in quiz.questions)
    assert "answer_key" not in payload["retrieval_quiz"]


def test_attempt_skip_request_is_redirected_into_attempt_first_boundary() -> None:
    session_id = _create_law_session()

    response = client.post(
        f"/sessions/{session_id}/attempt",
        json={
            "attempt_text": "Please just tell me the answer before I try anything.",
            "confidence_score": 1,
            "confusion_note": None,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["failure_analysis"]["failure_label"] == "unsupported_guess"
    assert "attempt" in payload["failure_analysis"]["missing_concept"].lower()


def test_get_session_trace_after_attempt_returns_safe_public_trace() -> None:
    session_id = _create_law_session()
    attempt_response = client.post(
        f"/sessions/{session_id}/attempt",
        json={
            "attempt_text": "This looks like a counter offer because the buyer changed the terms by adding the laptop bag.",
            "confidence_score": 4,
        },
    )
    assert attempt_response.status_code == 200

    trace_response = client.get(f"/sessions/{session_id}")

    assert trace_response.status_code == 200
    trace = trace_response.json()
    assert trace["session"]["status"] == "consolidated"
    assert trace["attempt"]["attempt_text"].startswith("This looks like")
    assert trace["failure_analysis"]["failure_label"] == "strong_attempt"
    assert trace["retrieval_quiz"] is not None
    assert trace["challenge"]["source"]["citation_label"].startswith("Sample")
    assert trace["failure_analysis"]["source"]["citation_label"].startswith("Sample")
    assert trace["retrieval_quiz"]["source"]["citation_label"].startswith("Sample")
    assert "answer_key" not in trace["retrieval_quiz"]


def test_submit_quiz_scores_answers_and_updates_session_status() -> None:
    session_id = _create_law_session()
    attempt_response = client.post(
        f"/sessions/{session_id}/attempt",
        json={
            "attempt_text": "This is not acceptance because the reply changes the offer terms, so it may be a counter offer.",
            "confidence_score": 4,
        },
    )
    assert attempt_response.status_code == 200
    questions = attempt_response.json()["retrieval_quiz"]["questions"]

    quiz_response = client.post(
        f"/sessions/{session_id}/quiz",
        json={
            "answers": [
                {"question_id": questions[0]["question_id"], "answer_text": "Acceptance must match the offer."},
                {"question_id": questions[1]["question_id"], "answer_text": "Changing material terms matters."},
                {"question_id": questions[2]["question_id"], "answer_text": "Apply the same rule to the new facts."},
            ]
        },
    )

    assert quiz_response.status_code == 200
    result = quiz_response.json()["quiz_result"]
    assert 0 <= result["score"] <= 1
    assert result["mastery_estimate"] in {"needs_review", "developing", "almost_there", "secure"}
    assert quiz_response.json()["recommended_next_step"]

    trace = client.get(f"/sessions/{session_id}").json()
    assert trace["session"]["status"] == "quiz_completed"
    assert trace["quiz_result"] is not None


def test_submit_quiz_before_attempt_is_rejected() -> None:
    session_id = _create_law_session()

    response = client.post(
        f"/sessions/{session_id}/quiz",
        json={
            "answers": [
                {"question_id": "q1", "answer_text": "one"},
                {"question_id": "q2", "answer_text": "two"},
                {"question_id": "q3", "answer_text": "three"},
            ]
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"]["error_code"] == "quiz_not_ready"
