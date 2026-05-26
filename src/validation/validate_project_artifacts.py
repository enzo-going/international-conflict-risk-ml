from __future__ import annotations

from pathlib import Path
import json
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)

REPORT_CSV_PATH = OUTPUT_TABLES_DIR / "project_validation_report.csv"
SUMMARY_JSON_PATH = OUTPUT_TABLES_DIR / "project_validation_summary.json"


REQUIRED_FILES = [
    "README.md",
    "docs/project_map.md",
    "docs/data_inventory.md",
    "docs/index.html",
    "docs/methodology/final_methodological_summary.md",
    "docs/methodology/modeling_notes.md",
    "docs/methodology/one_sided_experimental_module_review.md",
    "src/models/train_conflict_risk_model.py",
    "src/models/train_candidate_models.py",
    "src/data/build_sqlite_database.py",
    "sql/schema.sql",
    "outputs/tables/conflict_risk_model_metrics.csv",
    "outputs/tables/conflict_risk_model_test_predictions.csv",
    "outputs/tables/conflict_risk_model_coefficients.csv",
    "outputs/tables/candidate_model_comparison.csv",
    "outputs/models/conflict_risk_model_features.json",
]

OPTIONAL_EXPERIMENTAL_FILES = [
    "src/models/ml_onesided_violence.py",
    "data/raw/ucdp/OneSided_v25_1.xlsx",
    "data/final/UCDP_One-sided_Violence_Dataset_updated.csv",
    "outputs/tables/one_sided_predictions.csv",
    "outputs/tables/one_sided_feature_importance.csv",
    "outputs/tables/neighbors.json",
]


CSV_EXPECTATIONS = {
    "outputs/tables/conflict_risk_model_metrics.csv": [
        "model",
        "accuracy",
        "precision",
        "recall",
        "f1_score",
    ],
    "outputs/tables/conflict_risk_model_test_predictions.csv": [
        "country",
        "year",
        "target_conflict_next_year",
        "organized_violence_exists",
        "predicted_conflict_next_year",
        "predicted_conflict_probability",
    ],
    "outputs/tables/conflict_risk_model_coefficients.csv": [
        "rank",
        "feature",
        "feature_group",
        "coefficient",
        "absolute_coefficient",
        "effect",
    ],
    "outputs/tables/candidate_model_comparison.csv": [
        "model",
        "accuracy",
        "precision",
        "recall",
        "f1_score",
    ],
    "outputs/tables/one_sided_predictions.csv": [
        "location",
        "year",
        "target_next_year",
        "predicted",
        "probability",
    ],
    "outputs/tables/one_sided_feature_importance.csv": [
        "feature",
        "coefficient",
        "absolute_value",
    ],
}



PREDICTIVE_ANALYSIS_FILES = [
    "src/analysis/generate_predictive_analysis_report.py",
    "outputs/tables/predictive_top_risk_cases.csv",
    "outputs/tables/predictive_error_analysis.csv",
    "outputs/tables/predictive_region_summary.csv",
    "outputs/tables/predictive_country_summary.csv",
    "outputs/tables/predictive_threshold_summary.csv",
    "outputs/tables/predictive_analysis_summary.json",
    "reports/final/predictive_analysis_report.md",
]


PREDICTIVE_CHART_FILES = [
    "src/visualization/generate_predictive_charts.py",
    "outputs/charts/predictive_analysis/chart_index.json",
    "outputs/charts/predictive_analysis/threshold_f1_curve.png",
    "outputs/charts/predictive_analysis/threshold_precision_recall_curve.png",
    "outputs/charts/predictive_analysis/region_mean_predicted_probability.png",
    "outputs/charts/predictive_analysis/region_f1_score.png",
    "outputs/charts/predictive_analysis/risk_band_distribution.png",
    "outputs/charts/predictive_analysis/prediction_result_counts.png",
    "outputs/charts/predictive_analysis/top_countries_mean_predicted_probability.png",
    "outputs/charts/predictive_analysis/top_cases_predicted_probability.png",
]

CSV_EXPECTATIONS.update(
    {
        "outputs/tables/predictive_top_risk_cases.csv": [
            "country",
            "year",
            "region",
            "predicted_conflict_probability",
            "risk_band",
            "prediction_result",
        ],
        "outputs/tables/predictive_error_analysis.csv": [
            "country",
            "year",
            "region",
            "predicted_conflict_probability",
            "prediction_result",
        ],
        "outputs/tables/predictive_region_summary.csv": [
            "region",
            "cases",
            "countries",
            "mean_predicted_probability",
            "f1_score",
        ],
        "outputs/tables/predictive_country_summary.csv": [
            "country",
            "region",
            "years_observed",
            "mean_predicted_probability",
            "max_predicted_probability",
        ],
        "outputs/tables/predictive_threshold_summary.csv": [
            "threshold",
            "precision",
            "recall",
            "f1_score",
        ],
    }
)


def add_check(rows: list[dict], category: str, item: str, status: str, detail: str) -> None:
    rows.append(
        {
            "category": category,
            "item": item,
            "status": status,
            "detail": detail,
        }
    )


def validate_file_exists(rows: list[dict], relative_path: str, category: str) -> None:
    path = PROJECT_ROOT / relative_path

    if path.exists():
        add_check(rows, category, relative_path, "PASS", "file exists")
    else:
        add_check(rows, category, relative_path, "FAIL", "file missing")


def validate_csv_columns(rows: list[dict], relative_path: str, expected_columns: list[str]) -> None:
    path = PROJECT_ROOT / relative_path

    if not path.exists():
        add_check(rows, "csv_schema", relative_path, "SKIP", "file missing")
        return

    try:
        df = pd.read_csv(path)
    except Exception as error:
        add_check(rows, "csv_schema", relative_path, "FAIL", f"could not read csv: {error}")
        return

    missing_columns = [column for column in expected_columns if column not in df.columns]

    if missing_columns:
        add_check(
            rows,
            "csv_schema",
            relative_path,
            "FAIL",
            "missing columns: " + ", ".join(missing_columns),
        )
    else:
        add_check(
            rows,
            "csv_schema",
            relative_path,
            "PASS",
            f"rows={len(df)}, columns={len(df.columns)}",
        )


def validate_main_metrics(rows: list[dict]) -> None:
    path = PROJECT_ROOT / "outputs" / "tables" / "conflict_risk_model_metrics.csv"

    if not path.exists():
        add_check(rows, "model_metrics", "main_model", "SKIP", "metrics file missing")
        return

    df = pd.read_csv(path)

    required_columns = {"model", "f1_score"}
    if not required_columns.issubset(df.columns):
        add_check(rows, "model_metrics", "main_model", "FAIL", "required metric columns missing")
        return

    logistic_rows = df[df["model"].astype(str).str.contains("Logistic Regression", case=False, na=False)]
    baseline_rows = df[df["model"].astype(str).str.contains("Persistence", case=False, na=False)]

    if logistic_rows.empty:
        add_check(rows, "model_metrics", "main_model", "FAIL", "logistic regression row missing")
        return

    if baseline_rows.empty:
        add_check(rows, "model_metrics", "baseline", "FAIL", "persistence baseline row missing")
        return

    logistic_f1 = float(logistic_rows.iloc[0]["f1_score"])
    baseline_f1 = float(baseline_rows.iloc[0]["f1_score"])

    if logistic_f1 > baseline_f1:
        add_check(
            rows,
            "model_metrics",
            "main_model_vs_baseline",
            "PASS",
            f"logistic_f1={logistic_f1:.4f}, baseline_f1={baseline_f1:.4f}",
        )
    else:
        add_check(
            rows,
            "model_metrics",
            "main_model_vs_baseline",
            "WARN",
            f"logistic_f1={logistic_f1:.4f}, baseline_f1={baseline_f1:.4f}",
        )


def validate_features_metadata(rows: list[dict]) -> None:
    path = PROJECT_ROOT / "outputs" / "models" / "conflict_risk_model_features.json"

    if not path.exists():
        add_check(rows, "metadata", "conflict_risk_model_features.json", "FAIL", "file missing")
        return

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as error:
        add_check(rows, "metadata", "conflict_risk_model_features.json", "FAIL", f"invalid json: {error}")
        return

    target = data.get("target_column")
    n_features = data.get("n_features")
    features = data.get("feature_columns", [])

    if target != "target_conflict_next_year":
        add_check(rows, "metadata", "target_column", "FAIL", f"unexpected target: {target}")
    else:
        add_check(rows, "metadata", "target_column", "PASS", target)

    if isinstance(features, list) and len(features) == n_features:
        add_check(rows, "metadata", "feature_count", "PASS", f"n_features={n_features}")
    else:
        add_check(
            rows,
            "metadata",
            "feature_count",
            "WARN",
            f"n_features={n_features}, listed_features={len(features) if isinstance(features, list) else 'invalid'}",
        )


def main() -> None:
    rows: list[dict] = []

    for relative_path in REQUIRED_FILES:
        validate_file_exists(rows, relative_path, "required_file")

    for relative_path in OPTIONAL_EXPERIMENTAL_FILES:
        validate_file_exists(rows, relative_path, "experimental_file")

    for relative_path in PREDICTIVE_ANALYSIS_FILES:
        validate_file_exists(rows, relative_path, "predictive_analysis_file")

    for relative_path in PREDICTIVE_CHART_FILES:
        validate_file_exists(rows, relative_path, "predictive_chart_file")

    for relative_path, expected_columns in CSV_EXPECTATIONS.items():
        validate_csv_columns(rows, relative_path, expected_columns)

    validate_main_metrics(rows)
    validate_features_metadata(rows)

    report_df = pd.DataFrame(rows)
    report_df.to_csv(REPORT_CSV_PATH, index=False)

    status_counts = report_df["status"].value_counts().to_dict()

    summary = {
        "total_checks": int(len(report_df)),
        "status_counts": {str(key): int(value) for key, value in status_counts.items()},
        "report_csv": str(REPORT_CSV_PATH.relative_to(PROJECT_ROOT)),
    }

    SUMMARY_JSON_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Project artifact validation")
    print("---------------------------")
    print(f"Total checks: {summary['total_checks']}")
    for status, count in summary["status_counts"].items():
        print(f"{status}: {count}")

    print()
    print(f"Report CSV: {REPORT_CSV_PATH}")
    print(f"Summary JSON: {SUMMARY_JSON_PATH}")

    failures = status_counts.get("FAIL", 0)

    if failures:
        raise SystemExit(f"Validation completed with {failures} failure(s).")

    print()
    print("Validation completed without failures.")


if __name__ == "__main__":
    main()
