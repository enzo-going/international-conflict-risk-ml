from __future__ import annotations

import json
from pathlib import Path

import joblib
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

OUTPUT_MODELS_DIR = PROJECT_ROOT / "outputs" / "models"
OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"

MODEL_OUTPUT_PATH = OUTPUT_MODELS_DIR / "conflict_risk_logistic_regression_pipeline.joblib"
METRICS_OUTPUT_PATH = OUTPUT_TABLES_DIR / "conflict_risk_model_metrics.csv"
PREDICTIONS_OUTPUT_PATH = OUTPUT_TABLES_DIR / "conflict_risk_model_test_predictions.csv"
FEATURES_OUTPUT_PATH = OUTPUT_MODELS_DIR / "conflict_risk_model_features.json"

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

WORLD_BANK_RAW_COLUMNS = [
    "population_total",
    "gdp_per_capita_current_usd",
    "gdp_growth_annual_pct",
    "inflation_consumer_prices_annual_pct",
    "unemployment_total_pct",
    "military_expenditure_pct_gdp",
]


def get_engineered_world_bank_columns(df: pd.DataFrame) -> list[str]:
    return [
        column
        for column in df.columns
        if (
            column.endswith("_missing")
            or column.endswith("_lag1")
            or column.endswith("_change_1y")
            or column.endswith("_rolling_3y_mean")
        )
    ]


def evaluate_predictions(model_name: str, y_true: pd.Series, y_pred: pd.Series) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    return {
        "model": model_name,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1_score": f1_score(y_true, y_pred, zero_division=0),
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
    }


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


def main() -> None:
    OUTPUT_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    engineered_world_bank_columns = get_engineered_world_bank_columns(df)

    feature_columns = (
        BASE_FEATURE_COLUMNS
        + TEMPORAL_FEATURE_COLUMNS
        + WORLD_BANK_RAW_COLUMNS
        + engineered_world_bank_columns
    )

    train_mask = df["year"] <= TRAIN_END_YEAR
    test_mask = df["year"] > TRAIN_END_YEAR

    X_train = df.loc[train_mask, feature_columns]
    y_train = df.loc[train_mask, TARGET_COLUMN]

    X_test = df.loc[test_mask, feature_columns]
    y_test = df.loc[test_mask, TARGET_COLUMN]

    model = build_model()
    model.fit(X_train, y_train)

    y_pred_model = model.predict(X_test)
    y_proba_model = model.predict_proba(X_test)[:, 1]

    y_pred_persistence = df.loc[test_mask, "organized_violence_exists"]

    metrics = [
        evaluate_predictions(
            "Persistence baseline",
            y_test,
            y_pred_persistence,
        ),
        evaluate_predictions(
            "Logistic Regression scaled - World Bank engineered",
            y_test,
            y_pred_model,
        ),
    ]

    metrics_df = pd.DataFrame(metrics)

    baseline_f1 = metrics_df.loc[
        metrics_df["model"] == "Persistence baseline",
        "f1_score",
    ].iloc[0]

    metrics_df["f1_difference_vs_persistence"] = metrics_df["f1_score"] - baseline_f1

    predictions_df = df.loc[
        test_mask,
        [
            "country",
            "year",
            "region",
            "world_bank_country_code",
            "world_bank_country_name",
            TARGET_COLUMN,
            "organized_violence_exists",
        ],
    ].copy()

    predictions_df["predicted_conflict_next_year"] = y_pred_model
    predictions_df["predicted_conflict_probability"] = y_proba_model

    feature_metadata = {
        "target_column": TARGET_COLUMN,
        "train_end_year": TRAIN_END_YEAR,
        "test_start_year": int(df.loc[test_mask, "year"].min()),
        "test_end_year": int(df.loc[test_mask, "year"].max()),
        "n_features": len(feature_columns),
        "feature_columns": feature_columns,
        "model": "Pipeline(SimpleImputer median -> StandardScaler -> LogisticRegression balanced)",
    }

    joblib.dump(model, MODEL_OUTPUT_PATH)
    metrics_df.to_csv(METRICS_OUTPUT_PATH, index=False)
    predictions_df.to_csv(PREDICTIONS_OUTPUT_PATH, index=False)

    FEATURES_OUTPUT_PATH.write_text(
        json.dumps(feature_metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Conflict risk model trained successfully.")
    print(f"Input dataset: {DATA_PATH}")
    print(f"Train rows: {len(X_train)}")
    print(f"Test rows: {len(X_test)}")
    print(f"Features: {len(feature_columns)}")
    print()
    print("Metrics:")
    print(metrics_df.round(4).to_string(index=False))
    print()
    print(f"Saved model to: {MODEL_OUTPUT_PATH}")
    print(f"Saved metrics to: {METRICS_OUTPUT_PATH}")
    print(f"Saved predictions to: {PREDICTIONS_OUTPUT_PATH}")
    print(f"Saved feature metadata to: {FEATURES_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
