from __future__ import annotations

from dataclasses import dataclass

from app.models import FailureLabel


@dataclass(frozen=True)
class EvalCase:
    """A fixed diagnostic case for the mock learning engine boundary."""

    case_id: str
    concept_id: str
    attempt_text: str
    confidence_score: int
    confusion_note: str | None
    expected_labels: frozenset[FailureLabel]
    rationale: str


EVAL_CASES: tuple[EvalCase, ...] = (
    EvalCase(
        case_id="law_vague_offer_acceptance",
        concept_id="law_offer_acceptance",
        attempt_text="I think acceptance happens when both people agree somehow, but I am not sure when it becomes legally valid.",
        confidence_score=2,
        confusion_note="I am not sure when agreement becomes acceptance.",
        expected_labels=frozenset({FailureLabel.PARTIAL_PRIOR_KNOWLEDGE}),
        rationale="Vague agreement language should be treated as partial prior knowledge, not strong mastery.",
    ),
    EvalCase(
        case_id="law_strong_but_incomplete_offer_acceptance",
        concept_id="law_offer_acceptance",
        attempt_text="This is probably not acceptance because the reply changed material terms, so it may be a counter offer.",
        confidence_score=4,
        confusion_note="I am not fully sure how precise the legal wording should be.",
        expected_labels=frozenset({FailureLabel.STRONG_ATTEMPT}),
        rationale="The attempt identifies changed material terms and counter-offer logic.",
    ),
    EvalCase(
        case_id="commerce_calculation_without_reasoning",
        concept_id="commerce_break_even_analysis",
        attempt_text="I divide the numbers and get 40, but I am not sure why that operation is the correct one.",
        confidence_score=2,
        confusion_note="I can calculate but I do not know what the formula means.",
        expected_labels=frozenset({FailureLabel.CALCULATION_WITHOUT_REASONING}),
        rationale="The answer gives arithmetic without identifying fixed cost, variable cost, or contribution.",
    ),
    EvalCase(
        case_id="commerce_wrong_formula_application",
        concept_id="commerce_break_even_analysis",
        attempt_text="I would do 3000/120 = 25 units because the selling price is 120.",
        confidence_score=2,
        confusion_note="I am not sure whether variable cost matters.",
        expected_labels=frozenset({FailureLabel.MISAPPLIED_RULE_OR_FORMULA}),
        rationale="Using selling price instead of contribution per unit is the target formula error.",
    ),
    EvalCase(
        case_id="engineering_surface_level_moments",
        concept_id="engineering_moments",
        attempt_text="A bigger force makes the object turn more around the pivot.",
        confidence_score=2,
        confusion_note="I know force matters but I am unsure what else matters.",
        expected_labels=frozenset({FailureLabel.SURFACE_LEVEL_ANSWER}),
        rationale="The attempt names force but misses distance from the pivot.",
    ),
    EvalCase(
        case_id="python_lists_wrong_representation",
        concept_id="python_lists_sliding_window",
        attempt_text="I would store the ten readings in ten separate variables and shift each variable whenever a new reading arrives.",
        confidence_score=2,
        confusion_note="I am not sure if one variable can hold many readings.",
        expected_labels=frozenset({FailureLabel.WRONG_REPRESENTATION}),
        rationale="Separate variables are a brittle representation for a sliding window.",
    ),
    EvalCase(
        case_id="python_lists_near_correct_answer",
        concept_id="python_lists_sliding_window",
        attempt_text="Use a list, append the newest reading, and when there are more than ten readings remove the oldest first item.",
        confidence_score=4,
        confusion_note="I am not fully sure where the length check goes.",
        expected_labels=frozenset({FailureLabel.CORRECT_BUT_INCOMPLETE}),
        rationale="The representation is right but the update loop can still be tightened.",
    ),
    EvalCase(
        case_id="skip_attempt_answer_request",
        concept_id="law_offer_acceptance",
        attempt_text="Please just tell me the answer before I try anything.",
        confidence_score=1,
        confusion_note=None,
        expected_labels=frozenset({FailureLabel.UNSUPPORTED_GUESS}),
        rationale="The attempt-first boundary should redirect answer-seeking before effort.",
    ),
    EvalCase(
        case_id="unsupported_nonsense_answer",
        concept_id="law_offer_acceptance",
        attempt_text="Banana spaceship mirror thunder. I have no idea and I am guessing randomly.",
        confidence_score=1,
        confusion_note="This is a nonsense attempt.",
        expected_labels=frozenset({FailureLabel.MISSING_CORE_CONCEPT, FailureLabel.UNSUPPORTED_GUESS}),
        rationale="Nonsense should not be treated as strong or correct; the acceptable labels preserve current deterministic mock behaviour.",
    ),
    EvalCase(
        case_id="correct_answer_still_gets_transfer_quiz",
        concept_id="engineering_moments",
        attempt_text="The moment is 20 x 0.5, so the turning effect is 10 N m, and direction should also be stated.",
        confidence_score=5,
        confusion_note=None,
        expected_labels=frozenset({FailureLabel.STRONG_ATTEMPT}),
        rationale="Even a correct attempt should still receive transfer retrieval practice.",
    ),
)
