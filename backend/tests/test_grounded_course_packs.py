from __future__ import annotations

from app.concept_seed import SEEDED_CONCEPTS, SAMPLE_COURSE_PACKS
from app.models import QuestionType, SampleCoursePack


def test_sample_course_packs_are_valid_source_of_truth_fixtures() -> None:
    assert len(SAMPLE_COURSE_PACKS) == 4

    for course_pack in SAMPLE_COURSE_PACKS:
        validated = SampleCoursePack.model_validate(course_pack.model_dump())
        assert validated.source.title.startswith("Sample")
        assert validated.source.excerpt
        assert len(validated.rubric_items) >= 2
        assert len(validated.retrieval_questions) == 3
        assert any(
            question.question_type == QuestionType.SCENARIO_TRANSFER
            for question in validated.retrieval_questions
        )
        assert validated.canonical_answer
        assert validated.worked_example


def test_seeded_concepts_are_grounded_in_course_pack_sources_and_rubrics() -> None:
    for concept in SEEDED_CONCEPTS:
        assert concept.source.source_id
        assert concept.source.citation_label
        assert concept.source.excerpt
        assert len(concept.rubric_items) >= 2
        assert len(concept.retrieval_questions) == 3
        assert concept.retrieval_question_seeds == [
            question.question_text for question in concept.retrieval_questions
        ]


def test_quiz_answer_keys_are_present_in_course_packs_but_not_needed_for_concept_preview() -> None:
    for course_pack in SAMPLE_COURSE_PACKS:
        expected_answers = [question.expected_answer for question in course_pack.retrieval_questions]
        assert all(answer.strip() for answer in expected_answers)
