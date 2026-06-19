from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from app.models import (
    Concept,
    ConsolidationResponse,
    FailureAnalysis,
    FailureLabel,
    MasteryEstimate,
    QuizAnswer,
    QuizQuestion,
    QuizResultFeedback,
    QuizSubmittedAnswer,
    RubricItem,
    StoredRetrievalQuiz,
    StudentAttempt,
)
from app.time_utils import utc_now


@dataclass(frozen=True)
class RubricMatchResult:
    matched_items: list[RubricItem]
    missing_items: list[RubricItem]


class MockLearningEngine:
    """Deterministic source-grounded mock AI boundary.

    The engine does not call an LLM. It reads bundled sample course-pack fields,
    checks attempts against explicit rubric markers, and returns typed outputs.
    This keeps the demo inspectable while proving the correct product behaviour:
    questions, consolidation, and answer keys are grounded in source material.
    """

    def build_attempt_outputs(
        self,
        *,
        concept: Concept,
        attempt: StudentAttempt,
    ) -> tuple[FailureAnalysis, ConsolidationResponse, StoredRetrievalQuiz]:
        now = utc_now()
        rubric_result = self._match_rubric(concept=concept, attempt_text=attempt.attempt_text)
        failure_label, score, prior_knowledge, missing_concept, misconception = self._classify_attempt(
            concept=concept,
            attempt_text=attempt.attempt_text,
            rubric_result=rubric_result,
        )

        analysis = FailureAnalysis(
            analysis_id=str(uuid4()),
            attempt_id=attempt.attempt_id,
            failure_label=failure_label,
            prior_knowledge_detected=prior_knowledge,
            missing_concept=missing_concept,
            misconception_summary=misconception,
            productive_failure_score=score,
            feedback_strategy=self._feedback_strategy(failure_label),
            should_consolidate=True,
            source=concept.source,
            matched_rubric_items=[item.criterion for item in rubric_result.matched_items],
            missing_rubric_items=[item.feedback_if_missing for item in rubric_result.missing_items],
            created_at=now,
        )

        consolidation = self._build_consolidation(
            concept=concept,
            analysis=analysis,
            rubric_result=rubric_result,
            created_at=now,
        )
        quiz = self._build_quiz(concept=concept, session_id=attempt.session_id, created_at=now)
        return analysis, consolidation, quiz

    def score_quiz(
        self,
        *,
        quiz: StoredRetrievalQuiz,
        submitted_answers: list[QuizSubmittedAnswer],
    ) -> QuizResultFeedback:
        submitted_by_id = {answer.question_id: answer.answer_text.lower() for answer in submitted_answers}
        answer_key_by_id = {answer.question_id: answer for answer in quiz.answer_key}

        feedback: list[str] = []
        correct_count = 0
        for question_id, answer_key in answer_key_by_id.items():
            submitted = submitted_by_id.get(question_id, "")
            expected_tokens = self._content_tokens(answer_key.expected_answer)
            matched_tokens = [token for token in expected_tokens if token in submitted]
            is_correct = len(matched_tokens) >= max(1, min(2, len(expected_tokens)))
            source_note = f" Source: {answer_key.source_citation_label}." if answer_key.source_citation_label else ""
            if is_correct:
                correct_count += 1
                feedback.append(f"{question_id}: acceptable retrieval. {answer_key.scoring_guidance}{source_note}")
            else:
                feedback.append(f"{question_id}: revise this point. {answer_key.scoring_guidance}{source_note}")

        score = correct_count / len(answer_key_by_id)
        mastery = self._mastery_from_score(score)
        recommended_next_step = self._recommended_next_step(mastery)
        return QuizResultFeedback(
            result_id=str(uuid4()),
            quiz_id=quiz.quiz_id,
            session_id=quiz.session_id,
            score=score,
            feedback=feedback,
            mastery_estimate=mastery,
            recommended_next_step=recommended_next_step,
            created_at=utc_now(),
        )

    def _match_rubric(self, *, concept: Concept, attempt_text: str) -> RubricMatchResult:
        normalized = self._normalize(attempt_text)
        matched: list[RubricItem] = []
        missing: list[RubricItem] = []
        for item in concept.rubric_items:
            markers = [self._normalize(marker) for marker in item.expected_markers]
            if any(marker and marker in normalized for marker in markers):
                matched.append(item)
            else:
                missing.append(item)
        return RubricMatchResult(matched_items=matched, missing_items=missing)

    def _classify_attempt(
        self,
        *,
        concept: Concept,
        attempt_text: str,
        rubric_result: RubricMatchResult,
    ) -> tuple[FailureLabel, int, list[str], str, str]:
        text = attempt_text.lower()
        normalized = self._normalize(attempt_text)
        if any(phrase in text for phrase in ["just tell me", "give me the answer", "explain first"]):
            return (
                FailureLabel.UNSUPPORTED_GUESS,
                1,
                [],
                "A meaningful attempt must come before the full explanation.",
                "The response tries to bypass the attempt-first learning step.",
            )

        matched = rubric_result.matched_items
        missing = rubric_result.missing_items
        prior_knowledge = [item.criterion for item in matched] or ["engaged with the source-grounded challenge"]
        missing_feedback = missing[0].feedback_if_missing if missing else "Move from correctness into transfer practice."
        missing_concept = missing_feedback
        misconception = self._misconception_summary(concept=concept, missing_items=missing)

        if concept.concept_id == "law_offer_acceptance":
            if any(term in text for term in ["agree", "accepted", "sounds good"]) and not any(
                term in text for term in ["counter", "counter-offer", "changed", "material", "not acceptance", "not accepted"]
            ):
                return (
                    FailureLabel.PARTIAL_PRIOR_KNOWLEDGE,
                    3,
                    prior_knowledge,
                    "Acceptance must match the offer's material terms.",
                    "The answer treats interest in the deal as enough for acceptance unless changed terms are checked explicitly.",
                )

        if concept.concept_id == "commerce_break_even_analysis":
            matched_ids = {item.rubric_item_id for item in matched}
            if "contribution" in matched_ids and ("75" in normalized.split() or "contribution" in text):
                return (
                    FailureLabel.STRONG_ATTEMPT,
                    5,
                    prior_knowledge,
                    missing_concept,
                    "The contribution-per-unit structure is present; add fixed-cost division and units if missing.",
                )
            if "3000 120" in normalized or "3000/120" in text.replace(" ", "") or "25" in normalized.split():
                return (
                    FailureLabel.MISAPPLIED_RULE_OR_FORMULA,
                    2,
                    prior_knowledge,
                    "Break-even uses contribution per unit, not selling price.",
                    "The calculation ignores that each unit also has a variable cost.",
                )
            if any(token.isdigit() for token in normalized.split()) and len(matched) < 2:
                return (
                    FailureLabel.CALCULATION_WITHOUT_REASONING,
                    2,
                    prior_knowledge,
                    missing_concept,
                    "The answer gives arithmetic before identifying the cost structure.",
                )

        if concept.concept_id == "python_lists_sliding_window":
            matched_ids = {item.rubric_item_id for item in matched}
            if any(term in text for term in ["string", "ten variables", "separate variables"]):
                return (
                    FailureLabel.WRONG_REPRESENTATION,
                    2,
                    prior_knowledge,
                    "Use one ordered list rather than separate variables or a string.",
                    "The representation makes updates brittle once new readings arrive.",
                )
            if {"ordered_collection", "append_new", "remove_oldest"}.issubset(matched_ids) and "length_check" not in matched_ids:
                return (
                    FailureLabel.CORRECT_BUT_INCOMPLETE,
                    4,
                    prior_knowledge,
                    "Make the length check and add-then-trim loop explicit.",
                    "The representation is right, but the update rule still needs the exact condition for trimming the list.",
                )

        if concept.concept_id == "engineering_moments":
            if "force" in text and not any(item.rubric_item_id == "distance" for item in matched):
                return (
                    FailureLabel.SURFACE_LEVEL_ANSWER,
                    2,
                    prior_knowledge,
                    "The distance from the pivot is also required.",
                    "The answer describes pushing harder but misses lever arm distance.",
                )

        weighted_total = sum(item.weight for item in concept.rubric_items)
        weighted_matched = sum(item.weight for item in matched)
        ratio = weighted_matched / weighted_total if weighted_total else 0.0

        if ratio >= 0.8:
            return (
                FailureLabel.STRONG_ATTEMPT,
                5,
                prior_knowledge,
                missing_concept,
                "The core source-grounded rule is present; tighten precision and transfer it.",
            )
        if ratio >= 0.5:
            return (
                FailureLabel.CORRECT_BUT_INCOMPLETE,
                4,
                prior_knowledge,
                missing_concept,
                misconception,
            )
        if ratio > 0:
            return (
                FailureLabel.PARTIAL_PRIOR_KNOWLEDGE,
                3,
                prior_knowledge,
                missing_concept,
                misconception,
            )
        return (
            FailureLabel.MISSING_CORE_CONCEPT,
            2,
            prior_knowledge,
            missing_concept,
            misconception,
        )

    def _misconception_summary(self, *, concept: Concept, missing_items: list[RubricItem]) -> str:
        if not missing_items:
            return "The answer is mostly aligned with the sample source; the next step is transfer practice."
        first_missing = missing_items[0]
        return (
            f"The attempt has not yet shown this source-grounded criterion: {first_missing.criterion}. "
            f"{first_missing.feedback_if_missing}"
        )

    def _feedback_strategy(self, failure_label: FailureLabel) -> str:
        strategies = {
            FailureLabel.MISSING_CORE_CONCEPT: "Name the missing source-grounded concept, then connect it to the student's facts.",
            FailureLabel.MISAPPLIED_RULE_OR_FORMULA: "Preserve the useful setup, then correct the formula boundary using the course-pack rubric.",
            FailureLabel.WRONG_REPRESENTATION: "Compare the chosen representation with the source-backed canonical representation.",
            FailureLabel.UNSUPPORTED_GUESS: "Redirect to an attempt-first response without giving the full answer first.",
            FailureLabel.SURFACE_LEVEL_ANSWER: "Ask for the causal mechanism behind the surface observation.",
            FailureLabel.PARTIAL_PRIOR_KNOWLEDGE: "Turn the partial intuition into the formal source-grounded rule.",
            FailureLabel.CONFUSES_SIMILAR_CONCEPTS: "Separate the two concepts with a contrastive example from the source.",
            FailureLabel.CALCULATION_WITHOUT_REASONING: "Require variable identification before arithmetic.",
            FailureLabel.CORRECT_BUT_INCOMPLETE: "Acknowledge correctness and add the missing rubric criterion.",
            FailureLabel.STRONG_ATTEMPT: "Tighten precision and move quickly to transfer practice.",
        }
        return strategies[failure_label]

    def _build_consolidation(
        self,
        *,
        concept: Concept,
        analysis: FailureAnalysis,
        rubric_result: RubricMatchResult,
        created_at: datetime,
    ) -> ConsolidationResponse:
        first_question = concept.retrieval_questions[0]
        useful = [item.criterion for item in rubric_result.matched_items]
        missing = [item.feedback_if_missing for item in rubric_result.missing_items]
        return ConsolidationResponse(
            response_id=str(uuid4()),
            analysis_id=analysis.analysis_id,
            acknowledgement=(
                "You made the useful first move: you exposed your current understanding before receiving the explanation."
            ),
            what_was_useful=useful or ["You attempted the problem instead of waiting for the answer."],
            missing_or_confused=missing or ["No major rubric gap detected; now practise transfer without notes."],
            explanation=concept.canonical_explanation,
            worked_example=concept.worked_example,
            immediate_retrieval_prompt=first_question.question_text,
            source=concept.source,
            created_at=created_at,
        )

    def _build_quiz(
        self,
        *,
        concept: Concept,
        session_id: str,
        created_at: datetime,
    ) -> StoredRetrievalQuiz:
        quiz_id = str(uuid4())
        questions = [
            QuizQuestion(
                question_id=seed.question_id,
                question_text=seed.question_text,
                question_type=seed.question_type,
                source_citation_label=concept.source.citation_label,
            )
            for seed in concept.retrieval_questions
        ]
        answer_key = [
            QuizAnswer(
                question_id=seed.question_id,
                expected_answer=seed.expected_answer,
                scoring_guidance=seed.scoring_guidance,
                source_citation_label=concept.source.citation_label,
            )
            for seed in concept.retrieval_questions
        ]
        return StoredRetrievalQuiz(
            quiz_id=quiz_id,
            session_id=session_id,
            questions=questions,
            answer_key=answer_key,
            source=concept.source,
            created_at=created_at,
        )

    def _content_tokens(self, text: str) -> list[str]:
        ignored = {"the", "and", "or", "a", "an", "to", "of", "as", "is", "be", "for", "with", "that"}
        cleaned = self._normalize(text)
        return [token for token in cleaned.split() if len(token) > 3 and token not in ignored]

    def _normalize(self, text: str) -> str:
        return " ".join("".join(character.lower() if character.isalnum() else " " for character in text).split())

    def _mastery_from_score(self, score: float) -> MasteryEstimate:
        if score >= 0.99:
            return MasteryEstimate.SECURE
        if score >= 0.66:
            return MasteryEstimate.ALMOST_THERE
        if score >= 0.33:
            return MasteryEstimate.DEVELOPING
        return MasteryEstimate.NEEDS_REVIEW

    def _recommended_next_step(self, mastery: MasteryEstimate) -> str:
        if mastery == MasteryEstimate.SECURE:
            return "Move to a harder transfer problem and explain the rule without notes."
        if mastery == MasteryEstimate.ALMOST_THERE:
            return "Redo the transfer question and focus on the missing source-backed criterion."
        if mastery == MasteryEstimate.DEVELOPING:
            return "Review the consolidation, then answer a fresh retrieval question from the same source pack."
        return "Return to the worked example and write the source-grounded rule in your own words before retrying."
