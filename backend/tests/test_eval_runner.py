from __future__ import annotations

from app.evals.cases import EVAL_CASES
from app.evals.runner import report_to_dict, run_eval_cases


def test_eval_harness_runs_fixed_diagnostic_cases_successfully() -> None:
    report = run_eval_cases()

    assert report.summary.total_cases == 10
    assert report.summary.failed_cases == 0
    assert report.summary.pass_rate == 1.0
    assert {result.case_id for result in report.results} == {case.case_id for case in EVAL_CASES}


def test_eval_report_contains_required_output_fields() -> None:
    report = run_eval_cases()
    payload = report_to_dict(report)

    assert payload["summary"]["total_cases"] == 10
    assert payload["summary"]["passed_cases"] == 10
    assert payload["summary"]["failed_cases"] == 0
    assert payload["summary"]["pass_rate"] == 1.0

    first = payload["results"][0]
    assert set(first) == {
        "case_id",
        "passed",
        "failure_reason",
        "expected_label",
        "actual_label",
    }
