from __future__ import annotations

import json
from pathlib import Path

from app.models import Concept, SampleCoursePack


COURSE_PACK_DIR = Path(__file__).resolve().parent / "sample_course_packs"
COURSE_PACK_FILES = (
    "python_lists_sliding_window.json",
    "law_offer_acceptance.json",
    "commerce_break_even_analysis.json",
    "engineering_moments.json",
)


def load_sample_course_packs() -> tuple[SampleCoursePack, ...]:
    """Load bundled source-of-truth sample course packs.

    This is deliberately not a general upload/RAG pipeline. The packs are small,
    inspectable fixtures that make the demo source-grounded while preserving a
    deterministic no-API-key path.
    """

    packs: list[SampleCoursePack] = []
    for filename in COURSE_PACK_FILES:
        path = COURSE_PACK_DIR / filename
        payload = json.loads(path.read_text(encoding="utf-8"))
        packs.append(SampleCoursePack.model_validate(payload))
    return tuple(packs)


def concept_from_course_pack(course_pack: SampleCoursePack) -> Concept:
    return Concept(
        concept_id=course_pack.concept_id,
        title=course_pack.title,
        discipline=course_pack.discipline,
        module_context=course_pack.module_context,
        learning_outcome=course_pack.learning_outcome,
        prerequisite_knowledge=course_pack.prerequisite_knowledge,
        challenge_type=course_pack.challenge_type,
        challenge_prompt=course_pack.challenge_prompt,
        expected_reasoning_steps=course_pack.expected_reasoning_steps,
        common_misconceptions=course_pack.common_misconceptions,
        canonical_explanation=course_pack.canonical_explanation,
        retrieval_question_seeds=[question.question_text for question in course_pack.retrieval_questions],
        canonical_answer=course_pack.canonical_answer,
        worked_example=course_pack.worked_example,
        source=course_pack.source,
        rubric_items=course_pack.rubric_items,
        retrieval_questions=course_pack.retrieval_questions,
    )
