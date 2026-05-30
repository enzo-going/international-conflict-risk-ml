from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

EXPECTED_MAIN_F1 = 0.8722
EXPECTED_BASELINE_F1 = 0.8571
EXPECTED_FEATURE_COUNT = 33
EXPECTED_CHART_COUNT = 10
METRIC_TOLERANCE = 0.001


@dataclass
class Check:
    area: str
    name: str
    status: str
    detail: str


checks: list[Check] = []


def add_check(area: str, name: str, status: str, detail: str) -> None:
    checks.append(Check(area=area, name=name, status=status, detail=detail))


def project_path(relative_path: str) -> Path:
    return PROJECT_ROOT / relative_path


def chart_path_from_index(index_path: str, chart: str) -> str:
    if index_path.startswith("docs/") and chart.startswith("assets/"):
        return f"docs/{chart}"
    return chart


def check_exists(area: str, relative_path: str, required: bool = True) -> bool:
    path = project_path(relative_path)
    exists = path.exists()
    if exists:
        add_check(area, relative_path, "PASS", "exists")
    else:
        add_check(area, relative_path, "FAIL" if required else "WARN", "missing")
    return exists


def load_csv_dicts(relative_path: str) -> list[dict[str, str]]:
    path = project_path(relative_path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(relative_path: str) -> object:
    path = project_path(relative_path)
    return json.loads(path.read_text(encoding="utf-8-sig"))


def check_official_scripts() -> None:
    scripts = [
        "src/pipeline/run_official_pipeline.py",
        "scripts/run_official_pipeline.ps1",
        "src/data/build_conflict_country_year_base.py",
        "src/features/build_temporal_features.py",
        "src/data/build_conflict_country_year_world_bank.py",
        "src/features/build_world_bank_features.py",
        "src/models/train_conflict_risk_model.py",
        "src/visualization/generate_predictive_charts.py",
        "src/validation/validate_pipeline_state.py",
        "src/validation/validate_project_artifacts.py",
        "src/validation/validate_reproducibility_contract.py",
    ]

    for script in scripts:
        check_exists("official_scripts", script)


def check_official_outputs() -> None:
    outputs = [
        "data/final/conflict_country_year_base.csv",
        "data/final/conflict_country_year_temporal.csv",
        "data/final/conflict_country_year_world_bank.csv",
        "data/final/conflict_country_year_world_bank_features.csv",
        "outputs/models/conflict_risk_logistic_regression_pipeline.joblib",
        "outputs/models/conflict_risk_model_features.json",
        "outputs/tables/conflict_risk_model_metrics.csv",
        "outputs/tables/conflict_risk_model_test_predictions.csv",
        "outputs/tables/conflict_risk_model_coefficients.csv",
        "outputs/tables/probability_calibration_bins.csv",
        "outputs/tables/predictive_analysis_summary.json",
    ]

    for output in outputs:
        check_exists("official_outputs", output)


def check_metrics() -> None:
    metrics_path = "outputs/tables/conflict_risk_model_metrics.csv"
    if not check_exists("metrics", metrics_path):
        return

    try:
        rows = load_csv_dicts(metrics_path)
    except Exception as exc:  # noqa: BLE001
        add_check("metrics", "read_metrics_csv", "FAIL", str(exc))
        return

    main_rows = [
        row
        for row in rows
        if "Logistic Regression scaled - World Bank all raw" in row.get("model", "")
    ]
    baseline_rows = [
        row for row in rows if "Persistence baseline" in row.get("model", "")
    ]

    if not main_rows:
        add_check("metrics", "official_model_row", "FAIL", "official model row missing")
        return
    if not baseline_rows:
        add_check("metrics", "baseline_row", "FAIL", "persistence baseline row missing")
        return

    main_f1 = float(main_rows[0]["f1_score"])
    baseline_f1 = float(baseline_rows[0]["f1_score"])

    main_status = (
        "PASS" if abs(main_f1 - EXPECTED_MAIN_F1) <= METRIC_TOLERANCE else "FAIL"
    )
    baseline_status = (
        "PASS"
        if abs(baseline_f1 - EXPECTED_BASELINE_F1) <= METRIC_TOLERANCE
        else "FAIL"
    )
    comparison_status = "PASS" if main_f1 > baseline_f1 else "FAIL"

    add_check(
        "metrics",
        "official_f1",
        main_status,
        f"actual={main_f1:.4f}, expected~={EXPECTED_MAIN_F1:.4f}",
    )
    add_check(
        "metrics",
        "baseline_f1",
        baseline_status,
        f"actual={baseline_f1:.4f}, expected~={EXPECTED_BASELINE_F1:.4f}",
    )
    add_check(
        "metrics",
        "official_model_beats_baseline",
        comparison_status,
        f"official_f1={main_f1:.4f}, baseline_f1={baseline_f1:.4f}",
    )


def check_feature_metadata() -> None:
    metadata_path = "outputs/models/conflict_risk_model_features.json"
    if not check_exists("features", metadata_path):
        return

    try:
        metadata = load_json(metadata_path)
    except Exception as exc:  # noqa: BLE001
        add_check("features", "read_feature_metadata", "FAIL", str(exc))
        return

    n_features = int(metadata.get("n_features", -1))  # type: ignore[union-attr]
    feature_columns = metadata.get("feature_columns", [])  # type: ignore[union-attr]

    status = "PASS" if n_features == EXPECTED_FEATURE_COUNT else "FAIL"
    add_check(
        "features",
        "n_features",
        status,
        f"actual={n_features}, expected={EXPECTED_FEATURE_COUNT}",
    )

    status = "PASS" if len(feature_columns) == EXPECTED_FEATURE_COUNT else "FAIL"
    add_check(
        "features",
        "feature_columns_length",
        status,
        f"actual={len(feature_columns)}, expected={EXPECTED_FEATURE_COUNT}",
    )


def check_charts() -> None:
    chart_indexes = [
        "outputs/charts/predictive_analysis/chart_index.json",
        "docs/assets/charts/predictive_analysis/chart_index.json",
    ]

    for index_path in chart_indexes:
        if not check_exists("charts", index_path):
            continue

        try:
            chart_index = load_json(index_path)
            chart_count = int(chart_index.get("chart_count", -1))  # type: ignore[union-attr]
            charts = chart_index.get("charts", [])  # type: ignore[union-attr]
        except Exception as exc:  # noqa: BLE001
            add_check("charts", f"read_{index_path}", "FAIL", str(exc))
            continue

        status = "PASS" if chart_count == EXPECTED_CHART_COUNT else "FAIL"
        add_check(
            "charts",
            f"{index_path}:chart_count",
            status,
            f"actual={chart_count}, expected={EXPECTED_CHART_COUNT}",
        )

        status = "PASS" if len(charts) == EXPECTED_CHART_COUNT else "FAIL"
        add_check(
            "charts",
            f"{index_path}:listed_charts",
            status,
            f"actual={len(charts)}, expected={EXPECTED_CHART_COUNT}",
        )

        for chart in charts:
            check_exists("charts", chart_path_from_index(index_path, str(chart)))

    for calibration_chart in [
        "outputs/charts/predictive_analysis/probability_calibration_bins.png",
        "docs/assets/charts/predictive_analysis/probability_calibration_bins.png",
    ]:
        check_exists("charts", calibration_chart)


def check_docs_and_dashboard() -> None:
    docs = [
        "docs/methodology/consolidated_experimental_decision.md",
        "docs/methodology/probabilistic_risk_interpretation.md",
        "docs/methodology/model_training_pipeline.md",
        "docs/methodology/final_methodological_summary.md",
        "docs/project_map.md",
        "README.md",
        "docs/index.html",
    ]

    for doc in docs:
        check_exists("docs", doc)

    dashboard_path = project_path("docs/index.html")
    if not dashboard_path.exists():
        return

    dashboard = dashboard_path.read_text(encoding="utf-8")
    references = [
        "methodology/model_training_pipeline.md",
        "methodology/consolidated_experimental_decision.md",
        "methodology/probabilistic_risk_interpretation.md",
        "assets/charts/predictive_analysis/threshold_f1_curve.png",
        "assets/charts/predictive_analysis/probability_calibration_bins.png",
        "assets/charts/predictive_analysis/risk_band_distribution.png",
    ]

    for reference in references:
        status = "PASS" if reference in dashboard else "FAIL"
        add_check(
            "dashboard",
            f"references:{reference}",
            status,
            "referenced" if status == "PASS" else "not referenced",
        )


def print_report() -> int:
    status_order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    sorted_checks = sorted(
        checks,
        key=lambda check: (status_order.get(check.status, 99), check.area, check.name),
    )

    print("Reproducibility contract validation")
    print("-----------------------------------")
    print(f"Project root: {PROJECT_ROOT}")
    print()

    for check in sorted_checks:
        print(f"{check.status:4} {check.area}:{check.name} - {check.detail}")

    status_counts = {
        status: sum(1 for check in checks if check.status == status)
        for status in ("PASS", "WARN", "FAIL")
    }

    print()
    print("Summary")
    for status in ("PASS", "WARN", "FAIL"):
        print(f"{status}: {status_counts[status]}")

    return 1 if status_counts["FAIL"] else 0


def main() -> int:
    check_official_scripts()
    check_official_outputs()
    check_metrics()
    check_feature_metadata()
    check_charts()
    check_docs_and_dashboard()
    return print_report()


if __name__ == "__main__":
    sys.exit(main())
