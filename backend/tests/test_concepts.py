from fastapi.testclient import TestClient

from app.main import app
from app.models import ChallengeType, Concept, FailureLabel


client = TestClient(app)


def test_concepts_returns_four_discipline_agnostic_seeded_concepts() -> None:
    response = client.get("/concepts")

    assert response.status_code == 200
    payload = response.json()

    concepts = payload["concepts"]
    assert len(concepts) == 4

    concept_ids = {concept["concept_id"] for concept in concepts}
    assert concept_ids == {
        "python_lists_sliding_window",
        "law_offer_acceptance",
        "commerce_break_even_analysis",
        "engineering_moments",
    }

    disciplines = {concept["discipline"] for concept in concepts}
    assert disciplines == {
        "Computer Science",
        "Law",
        "Commerce",
        "Engineering and Physical Sciences",
    }


def test_seeded_concepts_validate_against_pydantic_contract() -> None:
    response = client.get("/concepts")
    payload = response.json()

    for raw_concept in payload["concepts"]:
        concept = Concept.model_validate(raw_concept)
        assert concept.challenge_type in set(ChallengeType)
        assert len(concept.retrieval_question_seeds) >= 3
        assert concept.canonical_explanation


def test_get_concept_returns_single_concept_by_id() -> None:
    response = client.get("/concepts/law_offer_acceptance")

    assert response.status_code == 200
    payload = response.json()

    assert payload["concept"]["concept_id"] == "law_offer_acceptance"
    assert payload["concept"]["discipline"] == "Law"
    assert payload["concept"]["challenge_type"] == "case_application"


def test_get_concept_returns_404_for_unknown_concept() -> None:
    response = client.get("/concepts/not_a_real_concept")

    assert response.status_code == 404
    assert response.json()["detail"] == {
        "error_code": "concept_not_found",
        "message": "No seeded concept exists for concept_id 'not_a_real_concept'.",
    }


def test_failure_labels_are_closed_enum_values_from_prd() -> None:
    assert {label.value for label in FailureLabel} == {
        "missing_core_concept",
        "misapplied_rule_or_formula",
        "wrong_representation",
        "unsupported_guess",
        "surface_level_answer",
        "partial_prior_knowledge",
        "confuses_similar_concepts",
        "calculation_without_reasoning",
        "correct_but_incomplete",
        "strong_attempt",
    }
