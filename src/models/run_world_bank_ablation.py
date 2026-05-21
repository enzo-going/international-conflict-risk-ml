from __future__ import annotations

from pathlib import Path

import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "final" / "conflict_country_year_world_bank_features.csv"

OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
OUTPUT_PATH = OUTPUT_TABLES_DIR / "world_bank_ablation_results.csv"

TARGET_COLUMN = "target_conflict_next_year"
TRAIN_END_YEAR = 2016


BASE_FEATURE_COLUMNS = [
    "year",
    "state_based_conflict_exists",
    "state_based_dyad_count",
    "state_based_deaths_best",
    "intrastate_conflict_exists",
    "intrastate_deaths_best",
    "interstate_conflict_exists",
    "interstate_deaths_best",
    "non_state_conflict_exists",
    "non_state_dyad_count",
    "non_state_deaths_best",
    "one_sided_violence_exists",
    "one_sided_dyad_count",
    "one_sided_deaths_best",
    "cumulative_organized_violence_deaths_best",
    "organized_violence_exists",
]


TEMPORAL_FEATURE_COLUMNS = [
    "conflict_previous_year",
    "conflict_last_3_years_count",
    "conflict_last_5_years_count",
    "deaths_previous_year",
    "deaths_last_3_years_sum",
    "deaths_last_5_years_sum",
    "years_since_last_conflict",
]


WORLD_BANK_WAVE_1_RAW_COLUMNS = [
    "population_total",
    "gdp_per_capita_current_usd",
    "gdp_growth_annual_pct",
    "inflation_consumer_prices_annual_pct",
    "unemployment_total_pct",
    "military_expenditure_pct_gdp",
]


WORLD_BANK_WAVE_2_RAW_COLUMNS = [
    "population_growth_annual_pct",
    "urban_population_pct",
    "school_enrollment_secondary_gross_pct",
    "natural_resources_rents_pct_gdp",
]


def get_engineered_columns_for_prefixes(
    df: pd.DataFrame,
    prefixes: list[str],
) -> list[str]:
    suffixes = (
        "_missing",
        "_lag1",
        "_change_1y",
        "_rolling_3y_mean",
    )

    selected_columns: list[str] = []

    for column in df.columns:
        for prefix in prefixes:
            if column.startswith(prefix) and column.endswith(suffixes):
                selected_columns.append(column)
                break

    return selected_columns


def validate_columns(df: pd.DataFrame, columns: list[str], context: str) -> None:
    missing_columns = [column for column in columns if column not in df.columns]

    if missing_columns:
        raise ValueError(
            f"Missing columns in {context}: {missing_columns}"
        )


def build_model() -> Pipeline:
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "model",
                LogisticRegression(
                    max_iter=5000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def evaluate_predictions(
    experiment: str,
    model_name: str,
    feature_count: int,
    y_true: pd.Series,
    y_pred: pd.Series,
    baseline_f1: float,
) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    f1 = f1_score(y_true, y_pred, zero_division=0)

    return {
        "experiment": experiment,
        "model": model_name,
        "feature_count": feature_count,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1_score": f1,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
        "f1_difference_vs_persistence": f1 - baseline_f1,
    }


def train_and_evaluate_experiment(
    df: pd.DataFrame,
    experiment: str,
    feature_columns: list[str],
    baseline_f1: float,
) -> dict:
    validate_columns(df, feature_columns, experiment)

    train_mask = df["year"] <= TRAIN_END_YEAR
    test_mask = df["year"] > TRAIN_END_YEAR

    X_train = df.loc[train_mask, feature_columns]
    y_train = df.loc[train_mask, TARGET_COLUMN]

    X_test = df.loc[test_mask, feature_columns]
    y_test = df.loc[test_mask, TARGET_COLUMN]

    model = build_model()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    return evaluate_predictions(
        experiment=experiment,
        model_name="Logistic Regression scaled",
        feature_count=len(feature_columns),
        y_true=y_test,
        y_pred=y_pred,
        baseline_f1=baseline_f1,
    )


def main() -> None:
    OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    validate_columns(
        df,
        [TARGET_COLUMN, "year", "organized_violence_exists"],
        "main dataset",
    )

    train_mask = df["year"] <= TRAIN_END_YEAR
    test_mask = df["year"] > TRAIN_END_YEAR

    y_test = df.loc[test_mask, TARGET_COLUMN]
    y_pred_persistence = df.loc[test_mask, "organized_violence_exists"]

    persistence_metrics_raw = evaluate_predictions(
        experiment="reference",
        model_name="Persistence baseline",
        feature_count=1,
        y_true=y_test,
        y_pred=y_pred_persistence,
        baseline_f1=0.0,
    )

    baseline_f1 = persistence_metrics_raw["f1_score"]
    persistence_metrics = persistence_metrics_raw.copy()
    persistence_metrics["f1_difference_vs_persistence"] = 0.0

    wave_1_engineered_columns = get_engineered_columns_for_prefixes(
        df,
        WORLD_BANK_WAVE_1_RAW_COLUMNS,
    )

    wave_2_engineered_columns = get_engineered_columns_for_prefixes(
        df,
        WORLD_BANK_WAVE_2_RAW_COLUMNS,
    )

    all_world_bank_raw_columns = (
        WORLD_BANK_WAVE_1_RAW_COLUMNS
        + WORLD_BANK_WAVE_2_RAW_COLUMNS
    )

    all_world_bank_engineered_columns = (
        wave_1_engineered_columns
        + wave_2_engineered_columns
    )

    experiments = [
        (
            "ucdp_base",
            BASE_FEATURE_COLUMNS,
        ),
        (
            "ucdp_temporal",
            BASE_FEATURE_COLUMNS
            + TEMPORAL_FEATURE_COLUMNS,
        ),
        (
            "world_bank_wave_1_raw",
            BASE_FEATURE_COLUMNS
            + TEMPORAL_FEATURE_COLUMNS
            + WORLD_BANK_WAVE_1_RAW_COLUMNS,
        ),
        (
            "world_bank_wave_1_engineered",
            BASE_FEATURE_COLUMNS
            + TEMPORAL_FEATURE_COLUMNS
            + WORLD_BANK_WAVE_1_RAW_COLUMNS
            + wave_1_engineered_columns,
        ),
        (
            "world_bank_wave_2_raw",
            BASE_FEATURE_COLUMNS
            + TEMPORAL_FEATURE_COLUMNS
            + WORLD_BANK_WAVE_2_RAW_COLUMNS,
        ),
        (
            "world_bank_wave_2_engineered",
            BASE_FEATURE_COLUMNS
            + TEMPORAL_FEATURE_COLUMNS
            + WORLD_BANK_WAVE_2_RAW_COLUMNS
            + wave_2_engineered_columns,
        ),
        (
            "world_bank_all_raw",
            BASE_FEATURE_COLUMNS
            + TEMPORAL_FEATURE_COLUMNS
            + all_world_bank_raw_columns,
        ),
        (
            "world_bank_all_engineered",
            BASE_FEATURE_COLUMNS
            + TEMPORAL_FEATURE_COLUMNS
            + all_world_bank_raw_columns
            + all_world_bank_engineered_columns,
        ),
    ]

    results = [persistence_metrics]

    for experiment_name, feature_columns in experiments:
        results.append(
            train_and_evaluate_experiment(
                df=df,
                experiment=experiment_name,
                feature_columns=feature_columns,
                baseline_f1=baseline_f1,
            )
        )

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by=["f1_score", "accuracy"],
        ascending=False,
    ).reset_index(drop=True)

    results_df.to_csv(OUTPUT_PATH, index=False)

    print("World Bank ablation analysis completed.")
    print(f"Input dataset: {DATA_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print()
    print(f"Train rows: {train_mask.sum()}")
    print(f"Test rows: {test_mask.sum()}")
    print()
    print("Feature group sizes:")
    print(f"- UCDP base: {len(BASE_FEATURE_COLUMNS)}")
    print(f"- UCDP temporal: {len(TEMPORAL_FEATURE_COLUMNS)}")
    print(f"- World Bank wave 1 raw: {len(WORLD_BANK_WAVE_1_RAW_COLUMNS)}")
    print(f"- World Bank wave 1 engineered: {len(wave_1_engineered_columns)}")
    print(f"- World Bank wave 2 raw: {len(WORLD_BANK_WAVE_2_RAW_COLUMNS)}")
    print(f"- World Bank wave 2 engineered: {len(wave_2_engineered_columns)}")
    print()
    print("Results:")
    print(
        results_df[
            [
                "experiment",
                "model",
                "feature_count",
                "accuracy",
                "precision",
                "recall",
                "f1_score",
                "f1_difference_vs_persistence",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()