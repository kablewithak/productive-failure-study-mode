from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.models import (
    Concept,
    ConsolidationResponse,
    FailureAnalysis,
    FailureLabel,
    MasteryEstimate,
    QuestionType,
    QuizAnswer,
    QuizQuestion,
    QuizResultFeedback,
    QuizSubmittedAnswer,
    StoredRetrievalQuiz,
    StudentAttempt,
)
from app.time_utils import utc_now


class MockLearningEngine:
    """Deterministic mock AI boundary for the Productive Failure loop.

    The goal is not model cleverness. The goal is stable structured outputs that
    can drive the frontend and eval harness without API keys.
    """

    def build_attempt_outputs(
        self,
        *,
        concept: Concept,
        attempt: StudentAttempt,
    ) -> tuple[FailureAnalysis, ConsolidationResponse, StoredRetrievalQuiz]:
        now = utc_now()
        failure_label, score, prior_knowledge, missing_concept, misconception = self._classify_attempt(
            concept=concept,
            attempt_text=attempt.attempt_text,
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
            created_at=now,
        )

        consolidation = self._build_consolidation(
            concept=concept,
            analysis=analysis,
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
            if is_correct:
                correct_count += 1
                feedback.append(f"{question_id}: acceptable retrieval. {answer_key.scoring_guidance}")
            else:
                feedback.append(f"{question_id}: revise this point. {answer_key.scoring_guidance}")

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

    def _classify_attempt(
        self,
        *,
        concept: Concept,
        attempt_text: str,
    ) -> tuple[FailureLabel, int, list[str], str, str]:
        text = attempt_text.lower()
        if any(phrase in text for phrase in ["just tell me", "give me the answer", "explain first"]):
            return (
                FailureLabel.UNSUPPORTED_GUESS,
                1,
                [],
                "A meaningful attempt must come before the full explanation.",
                "The response tries to bypass the attempt-first learning step.",
            )

        if concept.concept_id == "law_offer_acceptance":
            if any(term in text for term in ["counter", "not accept", "not acceptance", "changed", "material"]):
                return (
                    FailureLabel.STRONG_ATTEMPT,
                    5,
                    ["spotted that acceptance must match the offer"],
                    "Use precise acceptance versus counter-offer language.",
                    "The core rule is present; the answer can be tightened with legal terminology.",
                )
            if any(term in text for term in ["agree", "accepted", "sounds good"]):
                return (
                    FailureLabel.PARTIAL_PRIOR_KNOWLEDGE,
                    3,
                    ["recognized that agreement matters"],
                    "Acceptance must match the offer's material terms.",
                    "The answer treats interest in the deal as enough for acceptance.",
                )
            return (
                FailureLabel.MISSING_CORE_CONCEPT,
                2,
                ["engaged with the facts"],
                "The mirror-image idea behind acceptance is missing.",
                "The attempt does not yet separate negotiation from final agreement.",
            )

        if concept.concept_id == "commerce_break_even_analysis":
            if "75" in text or "contribution" in text or "120-45" in text.replace(" ", ""):
                return (
                    FailureLabel.STRONG_ATTEMPT,
                    5,
                    ["identified contribution per unit"],
                    "Round up units where a whole number of sales is required.",
                    "The core break-even structure is present.",
                )
            if "3000/120" in text.replace(" ", "") or "25" in text:
                return (
                    FailureLabel.MISAPPLIED_RULE_OR_FORMULA,
                    2,
                    ["recognized fixed cost must be recovered"],
                    "Break-even uses contribution per unit, not selling price.",
                    "The calculation ignores that each unit also has a variable cost.",
                )
            return (
                FailureLabel.CALCULATION_WITHOUT_REASONING,
                2,
                ["attempted a numerical solution"],
                "Separate fixed cost, selling price, and variable cost before calculating.",
                "The answer does not show why the chosen operation fits break-even.",
            )

        if concept.concept_id == "engineering_moments":
            if "10" in text or "20*0.5" in text.replace(" ", "") or "20 x 0.5" in text:
                return (
                    FailureLabel.STRONG_ATTEMPT,
                    5,
                    ["connected force and distance"],
                    "State the unit as newton-metres and mention direction where relevant.",
                    "The calculation is basically correct but should include interpretation.",
                )
            if "force" in text and "distance" not in text:
                return (
                    FailureLabel.SURFACE_LEVEL_ANSWER,
                    2,
                    ["recognized force matters"],
                    "The distance from the pivot is also required.",
                    "The answer describes pushing harder but misses lever arm distance.",
                )
            return (
                FailureLabel.MISSING_CORE_CONCEPT,
                2,
                ["identified a turning situation"],
                "Moment depends on force multiplied by perpendicular distance.",
                "The attempt does not yet connect turning effect to both variables.",
            )

        if concept.concept_id == "python_lists_sliding_window":
            if any(term in text for term in ["append", "pop", "remove first", "oldest", "len"]):
                return (
                    FailureLabel.CORRECT_BUT_INCOMPLETE,
                    4,
                    ["recognized the need for an ordered collection"],
                    "Make the add-then-trim loop explicit.",
                    "The answer is close but should state the full update rule.",
                )
            if any(term in text for term in ["string", "variable", "ten variables", "separate"]):
                return (
                    FailureLabel.WRONG_REPRESENTATION,
                    2,
                    ["recognized multiple readings must be stored"],
                    "Use one ordered list rather than separate variables or a string.",
                    "The representation makes updates brittle once new readings arrive.",
                )
            return (
                FailureLabel.PARTIAL_PRIOR_KNOWLEDGE,
                3,
                ["recognized that old readings must be discarded"],
                "Use a list as the state container for the sliding window.",
                "The attempt captures the goal but not the data structure.",
            )

        return (
            FailureLabel.UNSUPPORTED_GUESS,
            1,
            [],
            "No deterministic mock rule exists for this concept.",
            "The mock learning engine only supports seeded Phase 1 concepts.",
        )

    def _feedback_strategy(self, failure_label: FailureLabel) -> str:
        strategies = {
            FailureLabel.MISSING_CORE_CONCEPT: "Name the missing concept, then connect it to the student's facts.",
            FailureLabel.MISAPPLIED_RULE_OR_FORMULA: "Preserve the useful setup, then correct the formula boundary.",
            FailureLabel.WRONG_REPRESENTATION: "Compare the chosen representation with the canonical representation.",
            FailureLabel.UNSUPPORTED_GUESS: "Redirect to an attempt-first response without giving the full answer first.",
            FailureLabel.SURFACE_LEVEL_ANSWER: "Ask for the causal mechanism behind the surface observation.",
            FailureLabel.PARTIAL_PRIOR_KNOWLEDGE: "Turn the partial intuition into the formal rule.",
            FailureLabel.CONFUSES_SIMILAR_CONCEPTS: "Separate the two concepts with a contrastive example.",
            FailureLabel.CALCULATION_WITHOUT_REASONING: "Require variable identification before arithmetic.",
            FailureLabel.CORRECT_BUT_INCOMPLETE: "Acknowledge correctness and add the missing condition or interpretation.",
            FailureLabel.STRONG_ATTEMPT: "Tighten precision and move quickly to transfer practice.",
        }
        return strategies[failure_label]

    def _build_consolidation(
        self,
        *,
        concept: Concept,
        analysis: FailureAnalysis,
        created_at: datetime,
    ) -> ConsolidationResponse:
        first_seed = concept.retrieval_question_seeds[0]
        return ConsolidationResponse(
            response_id=str(uuid4()),
            analysis_id=analysis.analysis_id,
            acknowledgement=(
                "You made the useful first move: you exposed your current understanding before receiving the explanation."
            ),
            what_was_useful=analysis.prior_knowledge_detected or ["You attempted the problem instead of waiting for the answer."],
            missing_or_confused=[analysis.missing_concept, analysis.misconception_summary],
            explanation=concept.canonical_explanation,
            worked_example=self._worked_example(concept),
            immediate_retrieval_prompt=first_seed,
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
                question_id="q1",
                question_text=concept.retrieval_question_seeds[0],
                question_type=QuestionType.SHORT_ANSWER,
            ),
            QuizQuestion(
                question_id="q2",
                question_text=concept.retrieval_question_seeds[1],
                question_type=QuestionType.SHORT_ANSWER,
            ),
            QuizQuestion(
                question_id="q3",
                question_text=concept.retrieval_question_seeds[2],
                question_type=QuestionType.SCENARIO_TRANSFER,
            ),
        ]
        answer_key = [
            QuizAnswer(
                question_id="q1",
                expected_answer=concept.expected_reasoning_steps[0],
                scoring_guidance="Look for the core concept, not exact wording.",
            ),
            QuizAnswer(
                question_id="q2",
                expected_answer=concept.common_misconceptions[0],
                scoring_guidance="The answer should identify the trap or consequence.",
            ),
            QuizAnswer(
                question_id="q3",
                expected_answer=concept.expected_reasoning_steps[-1],
                scoring_guidance="The answer should transfer the rule to a new scenario.",
            ),
        ]
        return StoredRetrievalQuiz(
            quiz_id=quiz_id,
            session_id=session_id,
            questions=questions,
            answer_key=answer_key,
            created_at=created_at,
        )

    def _worked_example(self, concept: Concept) -> str:
        examples = {
            "law_offer_acceptance": (
                "If a seller offers a phone for R2,000 and the buyer replies, 'I accept for R2,000,' "
                "that is acceptance. If the buyer replies, 'I accept if you include headphones,' the buyer has changed the terms."
            ),
            "commerce_break_even_analysis": (
                "If fixed costs are R3,000 and each unit contributes R75 after variable cost, break-even is 3,000 / 75 = 40 units."
            ),
            "engineering_moments": (
                "A 20 N force applied 0.5 m from a pivot gives a moment of 20 x 0.5 = 10 N m."
            ),
            "python_lists_sliding_window": (
                "Keep readings in one list. Append the newest reading. If the list length becomes 11, remove index 0 so only 10 remain."
            ),
        }
        return examples.get(concept.concept_id, concept.canonical_explanation)

    def _content_tokens(self, text: str) -> list[str]:
        ignored = {"the", "and", "or", "a", "an", "to", "of", "as", "is", "be", "for"}
        cleaned = "".join(character.lower() if character.isalnum() else " " for character in text)
        return [token for token in cleaned.split() if len(token) > 3 and token not in ignored]

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
            return "Redo the transfer question and focus on the missing condition."
        if mastery == MasteryEstimate.DEVELOPING:
            return "Review the consolidation, then answer a fresh retrieval question."
        return "Return to the worked example and write the rule in your own words before retrying."
