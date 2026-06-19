from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from uuid import uuid4

from pydantic import ValidationError

from app.concept_seed import CONCEPTS_BY_ID
from app.evals.cases import EVAL_CASES, EvalCase
from app.models import (
    ConsolidationResponse,
    FailureAnalysis,
    QuestionType,
    RetrievalQuiz,
    StudentAttempt,
    SubmitAttemptResponse,
)
from app.services.mock_learning_engine import MockLearningEngine
from app.time_utils import utc_now


@dataclass(frozen=True)
class EvalCaseResult:
    case_id: str
    passed: bool
    failure_reason: str | None
    expected_label: str
    actual_label: str | None


@dataclass(frozen=True)
class EvalSummary:
    total_cases: int
    passed_cases: int
    failed_cases: int
    pass_rate: float


@dataclass(frozen=True)
class EvalReport:
    summary: EvalSummary
    results: list[EvalCaseResult]


def run_eval_cases(cases: tuple[EvalCase, ...] = EVAL_CASES) -> EvalReport:
    engine = MockLearningEngine()
    results = [_run_one_case(engine=engine, case=case) for case in cases]
    passed_cases = sum(1 for result in results if result.passed)
    total_cases = len(results)
    summary = EvalSummary(
        total_cases=total_cases,
        passed_cases=passed_cases,
        failed_cases=total_cases - passed_cases,
        pass_rate=round(passed_cases / total_cases, 3) if total_cases else 0.0,
    )
    return EvalReport(summary=summary, results=results)


def _run_one_case(*, engine: MockLearningEngine, case: EvalCase) -> EvalCaseResult:
    concept = CONCEPTS_BY_ID[case.concept_id]
    attempt = StudentAttempt(
        attempt_id=str(uuid4()),
        session_id=f"eval-{case.case_id}",
        attempt_text=case.attempt_text,
        confidence_score=case.confidence_score,
        confusion_note=case.confusion_note,
        created_at=utc_now(),
    )

    try:
        analysis, consolidation, stored_quiz = engine.build_attempt_outputs(
            concept=concept,
            attempt=attempt,
        )
        public_quiz = RetrievalQuiz(
            quiz_id=stored_quiz.quiz_id,
            session_id=stored_quiz.session_id,
            questions=stored_quiz.questions,
            source=stored_quiz.source,
            created_at=stored_quiz.created_at,
        )
        response = SubmitAttemptResponse(
            attempt_id=attempt.attempt_id,
            failure_analysis=analysis,
            consolidation=consolidation,
            retrieval_quiz=public_quiz,
        )

        checks = _evaluate_response(case=case, response=response)
        if checks:
            return EvalCaseResult(
                case_id=case.case_id,
                passed=False,
                failure_reason="; ".join(checks),
                expected_label=_expected_label_text(case),
                actual_label=response.failure_analysis.failure_label.value,
            )
        return EvalCaseResult(
            case_id=case.case_id,
            passed=True,
            failure_reason=None,
            expected_label=_expected_label_text(case),
            actual_label=response.failure_analysis.failure_label.value,
        )
    except (KeyError, ValidationError, ValueError) as exc:
        return EvalCaseResult(
            case_id=case.case_id,
            passed=False,
            failure_reason=f"schema_or_runtime_error: {exc}",
            expected_label=_expected_label_text(case),
            actual_label=None,
        )


def _evaluate_response(*, case: EvalCase, response: SubmitAttemptResponse) -> list[str]:
    failures: list[str] = []

    # Explicit Pydantic re-validation at the eval boundary.
    FailureAnalysis.model_validate(response.failure_analysis.model_dump())
    ConsolidationResponse.model_validate(response.consolidation.model_dump())
    RetrievalQuiz.model_validate(response.retrieval_quiz.model_dump())
    SubmitAttemptResponse.model_validate(response.model_dump())

    actual_label = response.failure_analysis.failure_label
    if actual_label not in case.expected_labels:
        failures.append(
            f"failure_label_mismatch expected={_expected_label_text(case)} actual={actual_label.value}"
        )

    if not response.consolidation.explanation.strip():
        failures.append("missing_consolidation_explanation")
    if not response.consolidation.worked_example.strip():
        failures.append("missing_worked_example")
    if not response.consolidation.immediate_retrieval_prompt.strip():
        failures.append("missing_immediate_retrieval_prompt")

    quiz = response.retrieval_quiz
    if len(quiz.questions) != 3:
        failures.append(f"quiz_question_count expected=3 actual={len(quiz.questions)}")
    if not any(question.question_type == QuestionType.SCENARIO_TRANSFER for question in quiz.questions):
        failures.append("missing_transfer_question")

    response_payload = response.model_dump(mode="json")
    if _contains_key(response_payload, "answer_key"):
        failures.append("answer_key_exposed_before_quiz_submission")

    if _looks_like_full_answer_leak(case=case, response=response):
        failures.append("direct_full_answer_given_before_attempt_boundary")

    if actual_label.value not in response.consolidation.missing_or_confused[0].lower() and not response.failure_analysis.feedback_strategy:
        failures.append("feedback_not_connected_to_failure_label")

    return failures


def _contains_key(value: object, key: str) -> bool:
    if isinstance(value, dict):
        return key in value or any(_contains_key(child, key) for child in value.values())
    if isinstance(value, list):
        return any(_contains_key(child, key) for child in value)
    return False


def _looks_like_full_answer_leak(*, case: EvalCase, response: SubmitAttemptResponse) -> bool:
    # The pre-attempt boundary is covered by create-session tests. Here we only
    # guard the special skip-attempt case: the system may redirect, but should
    # not hand over a direct canonical answer as if the attempt was valid.
    if case.case_id != "skip_attempt_answer_request":
        return False
    explanation = response.consolidation.explanation.lower()
    return "seller offers" in explanation and "buyer replies" in explanation


def _expected_label_text(case: EvalCase) -> str:
    return ",".join(sorted(label.value for label in case.expected_labels))


def report_to_dict(report: EvalReport) -> dict[str, object]:
    return {
        "summary": asdict(report.summary),
        "results": [asdict(result) for result in report.results],
    }


def print_report(report: EvalReport) -> None:
    for result in report.results:
        status = "PASS" if result.passed else "FAIL"
        reason = result.failure_reason or ""
        print(
            f"{result.case_id}\t{status}\texpected={result.expected_label}\tactual={result.actual_label}\t{reason}"
        )
    print(json.dumps(asdict(report.summary), indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Productive Failure mock-AI eval cases.")
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Optional path for a JSON eval report. Parent directories are created automatically.",
    )
    args = parser.parse_args()

    report = run_eval_cases()
    print_report(report)

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report_to_dict(report), indent=2), encoding="utf-8")

    return 0 if report.summary.failed_cases == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
