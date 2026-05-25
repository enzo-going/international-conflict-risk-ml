from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "final" / "conflict_country_year_world_bank_features.csv"
FEATURE_METADATA_PATH = PROJECT_ROOT / "outputs" / "models" / "conflict_risk_model_features.json"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "tables" / "candidate_model_comparison.csv"

TARGET_COLUMN = "target_conflict_next_year"
PERSISTENCE_COLUMN = "organized_violence_exists"


def load_feature_metadata() -> dict[str, Any]:
    if not FEATURE_METADATA_PATH.exists():
        raise FileNotFoundError(f"Feature metadata not found: {FEATURE_METADATA_PATH}")

    return json.loads(FEATURE_METADATA_PATH.read_text(encoding="utf-8"))


def build_models(random_state: int = 42) -> dict[str, Pipeline]:
    return {
        "Logistic Regression scaled - World Bank all raw": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=2000,
                        class_weight="balanced",
                        random_state=random_state,
                    ),
                ),
            ]
        ),
        "Random Forest - World Bank all raw": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=400,
                        max_depth=8,
                        min_samples_leaf=8,
                        class_weight="balanced",
                        random_state=random_state,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "Gradient Boosting - World Bank all raw": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "classifier",
                    GradientBoostingClassifier(
                        n_estimators=250,
                        learning_rate=0.03,
                        max_depth=3,
                        random_state=random_state,
                    ),
                ),
            ]
        ),
        "MLP scaled - World Bank all raw": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    MLPClassifier(
                        hidden_layer_sizes=(32, 16),
                        activation="relu",
                        alpha=0.001,
                        learning_rate_init=0.001,
                        max_iter=800,
                        early_stopping=True,
                        random_state=random_state,
                    ),
                ),
            ]
        ),
    }


def evaluate_predictions(
    model_name: str,
    y_true: pd.Series,
    y_pred: pd.Series,
    persistence_f1: float,
    feature_count: int,
) -> dict[str, Any]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    f1 = f1_score(y_true, y_pred, zero_division=0)

    return {
        "model": model_name,
        "feature_count": feature_count,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1_score": f1,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
        "f1_difference_vs_persistence": f1 - persistence_f1,
    }


def main() -> None:
    metadata = load_feature_metadata()

    feature_columns = metadata["feature_columns"]
    train_end_year = int(metadata.get("train_end_year", 2016))
    test_start_year = int(metadata.get("test_start_year", 2017))
    test_end_year = int(metadata.get("test_end_year", 2023))

    df = pd.read_csv(DATA_PATH)

    required_columns = feature_columns + [TARGET_COLUMN, PERSISTENCE_COLUMN, "year"]
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = df.dropna(subset=[TARGET_COLUMN]).copy()

    train_mask = df["year"] <= train_end_year
    test_mask = (df["year"] >= test_start_year) & (df["year"] <= test_end_year)

    train_df = df.loc[train_mask].copy()
    test_df = df.loc[test_mask].copy()

    X_train = train_df[feature_columns]
    y_train = train_df[TARGET_COLUMN].astype(int)

    X_test = test_df[feature_columns]
    y_test = test_df[TARGET_COLUMN].astype(int)

    persistence_pred = test_df[PERSISTENCE_COLUMN].astype(int)
    persistence_f1 = f1_score(y_test, persistence_pred, zero_division=0)

    results: list[dict[str, Any]] = []

    results.append(
        evaluate_predictions(
            model_name="Persistence baseline",
            y_true=y_test,
            y_pred=persistence_pred,
            persistence_f1=persistence_f1,
            feature_count=1,
        )
    )

    models = build_models()

    for model_name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        results.append(
            evaluate_predictions(
                model_name=model_name,
                y_true=y_test,
                y_pred=pd.Series(y_pred),
                persistence_f1=persistence_f1,
                feature_count=len(feature_columns),
            )
        )

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("f1_score", ascending=False)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_PATH, index=False)

    print("Candidate model comparison completed.")
    print(f"Input dataset: {DATA_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print()
    print(f"Train rows: {len(train_df)}")
    print(f"Test rows: {len(test_df)}")
    print(f"Features: {len(feature_columns)}")
    print(f"Train years: <= {train_end_year}")
    print(f"Test years: {test_start_year} - {test_end_year}")
    print()
    print("Results:")
    print(
        results_df[
            [
                "model",
                "feature_count",
                "accuracy",
                "precision",
                "recall",
                "f1_score",
                "f1_difference_vs_persistence",
            ]
        ].round(4).to_string(index=False)
    )


if __name__ == "__main__":
    main()