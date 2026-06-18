from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ChallengeType(StrEnum):
    SCENARIO_ANALYSIS = "scenario_analysis"
    CALCULATION_ATTEMPT = "calculation_attempt"
    CONCEPT_EXPLANATION = "concept_explanation"
    CASE_APPLICATION = "case_application"
    COMPARE_AND_CONTRAST = "compare_and_contrast"
    DIAGNOSE_ERROR = "diagnose_error"
    SHORT_PROBLEM_SOLVING = "short_problem_solving"


class FailureLabel(StrEnum):
    MISSING_CORE_CONCEPT = "missing_core_concept"
    MISAPPLIED_RULE_OR_FORMULA = "misapplied_rule_or_formula"
    WRONG_REPRESENTATION = "wrong_representation"
    UNSUPPORTED_GUESS = "unsupported_guess"
    SURFACE_LEVEL_ANSWER = "surface_level_answer"
    PARTIAL_PRIOR_KNOWLEDGE = "partial_prior_knowledge"
    CONFUSES_SIMILAR_CONCEPTS = "confuses_similar_concepts"
    CALCULATION_WITHOUT_REASONING = "calculation_without_reasoning"
    CORRECT_BUT_INCOMPLETE = "correct_but_incomplete"
    STRONG_ATTEMPT = "strong_attempt"


class SessionStatus(StrEnum):
    CREATED = "created"
    ATTEMPT_SUBMITTED = "attempt_submitted"
    CONSOLIDATED = "consolidated"
    QUIZ_COMPLETED = "quiz_completed"
    ABANDONED = "abandoned"


class HealthResponse(BaseModel):
    status: str = Field(description="Health status for the API process.")
    service: str = Field(description="Stable service identifier.")


class Concept(BaseModel):
    model_config = ConfigDict(frozen=True)

    concept_id: str = Field(min_length=3)
    title: str = Field(min_length=3)
    discipline: str = Field(min_length=3)
    module_context: str = Field(min_length=3)
    learning_outcome: str = Field(min_length=10)
    prerequisite_knowledge: list[str] = Field(min_length=1)
    challenge_type: ChallengeType
    challenge_prompt: str = Field(min_length=20)
    expected_reasoning_steps: list[str] = Field(min_length=1)
    common_misconceptions: list[str] = Field(min_length=1)
    canonical_explanation: str = Field(min_length=50)
    retrieval_question_seeds: list[str] = Field(min_length=3)


class ChallengePreview(BaseModel):
    concept_id: str
    challenge_type: ChallengeType
    challenge_prompt: str


class ConceptListResponse(BaseModel):
    concepts: list[Concept]


class ConceptResponse(BaseModel):
    concept: Concept


class ApiError(BaseModel):
    error_code: str
    message: str
