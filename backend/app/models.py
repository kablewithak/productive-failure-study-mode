from __future__ import annotations

from datetime import datetime
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


class QuestionType(StrEnum):
    SHORT_ANSWER = "short_answer"
    MULTIPLE_CHOICE = "multiple_choice"
    SCENARIO_TRANSFER = "scenario_transfer"
    CALCULATION = "calculation"


class MasteryEstimate(StrEnum):
    NEEDS_REVIEW = "needs_review"
    DEVELOPING = "developing"
    ALMOST_THERE = "almost_there"
    SECURE = "secure"


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


class ConceptSummary(BaseModel):
    concept_id: str
    title: str
    discipline: str
    module_context: str
    learning_outcome: str
    challenge_type: ChallengeType


class ConceptListResponse(BaseModel):
    concepts: list[Concept]


class ConceptResponse(BaseModel):
    concept: Concept


class LearningSession(BaseModel):
    session_id: str
    concept_id: str
    student_alias: str | None = Field(default=None, max_length=80)
    status: SessionStatus
    created_at: datetime
    updated_at: datetime


class CreateSessionRequest(BaseModel):
    concept_id: str = Field(min_length=3)
    student_alias: str | None = Field(default=None, max_length=80)


class CreateSessionResponse(BaseModel):
    session_id: str
    concept: ConceptSummary
    challenge: ChallengePreview


class SubmitAttemptRequest(BaseModel):
    attempt_text: str = Field(min_length=10, max_length=4000)
    confidence_score: int = Field(ge=1, le=5)
    confusion_note: str | None = Field(default=None, max_length=1000)


class StudentAttempt(BaseModel):
    attempt_id: str
    session_id: str
    attempt_text: str
    confidence_score: int = Field(ge=1, le=5)
    confusion_note: str | None = None
    created_at: datetime


class FailureAnalysis(BaseModel):
    analysis_id: str
    attempt_id: str
    failure_label: FailureLabel
    prior_knowledge_detected: list[str]
    missing_concept: str
    misconception_summary: str
    productive_failure_score: int = Field(ge=1, le=5)
    feedback_strategy: str
    should_consolidate: bool
    created_at: datetime


class ConsolidationResponse(BaseModel):
    response_id: str
    analysis_id: str
    acknowledgement: str
    what_was_useful: list[str]
    missing_or_confused: list[str]
    explanation: str
    worked_example: str
    immediate_retrieval_prompt: str
    created_at: datetime


class QuizQuestion(BaseModel):
    question_id: str
    question_text: str
    question_type: QuestionType
    options: list[str] | None = None


class QuizAnswer(BaseModel):
    question_id: str
    expected_answer: str
    scoring_guidance: str


class RetrievalQuiz(BaseModel):
    quiz_id: str
    session_id: str
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)
    created_at: datetime


class StoredRetrievalQuiz(RetrievalQuiz):
    answer_key: list[QuizAnswer] = Field(min_length=3, max_length=3)


class SubmitAttemptResponse(BaseModel):
    attempt_id: str
    failure_analysis: FailureAnalysis
    consolidation: ConsolidationResponse
    retrieval_quiz: RetrievalQuiz


class QuizSubmittedAnswer(BaseModel):
    question_id: str
    answer_text: str = Field(min_length=1, max_length=2000)


class SubmitQuizRequest(BaseModel):
    answers: list[QuizSubmittedAnswer] = Field(min_length=3, max_length=3)


class QuizResultFeedback(BaseModel):
    result_id: str
    quiz_id: str
    session_id: str
    score: float = Field(ge=0.0, le=1.0)
    feedback: list[str]
    mastery_estimate: MasteryEstimate
    recommended_next_step: str
    created_at: datetime


class SubmitQuizResponse(BaseModel):
    quiz_result: QuizResultFeedback
    recommended_next_step: str


class FailureLabelDistributionItem(BaseModel):
    failure_label: FailureLabel
    count: int = Field(ge=0)


class ConceptAttemptSummary(BaseModel):
    concept_id: str
    title: str
    discipline: str
    attempt_count: int = Field(ge=0)


class RecentLearningEvent(BaseModel):
    session_id: str
    concept_id: str
    concept_title: str
    discipline: str
    status: SessionStatus
    failure_label: FailureLabel | None = None
    confidence_score: int | None = Field(default=None, ge=1, le=5)
    quiz_score: float | None = Field(default=None, ge=0.0, le=1.0)
    created_at: datetime
    updated_at: datetime


class DashboardMetricsResponse(BaseModel):
    total_sessions: int = Field(ge=0)
    completed_sessions: int = Field(ge=0)
    average_confidence_score: float | None = Field(default=None, ge=1.0, le=5.0)
    average_quiz_score: float | None = Field(default=None, ge=0.0, le=1.0)
    failure_label_distribution: list[FailureLabelDistributionItem]
    recent_learning_events: list[RecentLearningEvent]
    concepts_attempted: list[ConceptAttemptSummary]


class SessionTraceResponse(BaseModel):
    session: LearningSession
    concept: ConceptSummary
    challenge: ChallengePreview
    attempt: StudentAttempt | None = None
    failure_analysis: FailureAnalysis | None = None
    consolidation: ConsolidationResponse | None = None
    retrieval_quiz: RetrievalQuiz | None = None
    quiz_result: QuizResultFeedback | None = None


class ApiError(BaseModel):
    error_code: str
    message: str
