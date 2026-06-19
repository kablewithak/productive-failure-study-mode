from __future__ import annotations

from app.course_packs import concept_from_course_pack, load_sample_course_packs
from app.models import Concept, SampleCoursePack


SAMPLE_COURSE_PACKS: tuple[SampleCoursePack, ...] = load_sample_course_packs()
SEEDED_CONCEPTS: tuple[Concept, ...] = tuple(
    concept_from_course_pack(course_pack) for course_pack in SAMPLE_COURSE_PACKS
)
CONCEPTS_BY_ID: dict[str, Concept] = {concept.concept_id: concept for concept in SEEDED_CONCEPTS}
COURSE_PACKS_BY_CONCEPT_ID: dict[str, SampleCoursePack] = {
    course_pack.concept_id: course_pack for course_pack in SAMPLE_COURSE_PACKS
}
