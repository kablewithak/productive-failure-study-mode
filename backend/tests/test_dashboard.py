from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.models import DashboardMetricsResponse


client = TestClient(app)


def test_dashboard_starts_with_valid_metrics_contract() -> None:
    response = client.get("/dashboard")

    assert response.status_code == 200
    payload = DashboardMetricsResponse.model_validate(response.json())
    assert payload.total_sessions >= 0
    assert payload.completed_sessions >= 0
    assert payload.completed_sessions <= payload.total_sessions


def test_dashboard_updates_after_completed_learning_session_without_student_alias_leakage() -> None:
    before_total = client.get("/dashboard").json()["total_sessions"]
    create_response = client.post(
        "/sessions",
        json={"concept_id": "commerce_break_even_analysis", "student_alias": "private-demo-name"},
    )
    assert create_response.status_code == 201
    session_id = create_response.json()["session_id"]

    attempt_response = client.post(
        f"/sessions/{session_id}/attempt",
        json={
            "attempt_text": "I think contribution is selling price minus variable cost, so 120 minus 45 gives 75 per unit.",
            "confidence_score": 4,
            "confusion_note": "I am not fully sure when to round units.",
        },
    )
    assert attempt_response.status_code == 200
    questions = attempt_response.json()["retrieval_quiz"]["questions"]

    quiz_response = client.post(
        f"/sessions/{session_id}/quiz",
        json={
            "answers": [
                {"question_id": questions[0]["question_id"], "answer_text": "Contribution per unit is selling price minus variable cost."},
                {"question_id": questions[1]["question_id"], "answer_text": "Using selling price alone ignores variable cost."},
                {"question_id": questions[2]["question_id"], "answer_text": "Transfer the same break-even rule to the new numbers."},
            ]
        },
    )
    assert quiz_response.status_code == 200

    dashboard_response = client.get("/dashboard")
    assert dashboard_response.status_code == 200
    dashboard = dashboard_response.json()
    DashboardMetricsResponse.model_validate(dashboard)

    assert dashboard["total_sessions"] >= before_total + 1
    assert dashboard["completed_sessions"] >= 1
    assert dashboard["average_confidence_score"] is not None
    assert dashboard["average_quiz_score"] is not None
    assert any(
        item["failure_label"] == "strong_attempt"
        for item in dashboard["failure_label_distribution"]
    )
    assert any(
        item["concept_id"] == "commerce_break_even_analysis"
        for item in dashboard["concepts_attempted"]
    )
    assert dashboard["recent_learning_events"]
    assert "student_alias" not in dashboard["recent_learning_events"][0]
