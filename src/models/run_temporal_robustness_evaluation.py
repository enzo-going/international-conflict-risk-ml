from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "final" / "conflict_country_year_world_bank_features.csv"
FEATURES_PATH = PROJECT_ROOT / "outputs" / "models" / "conflict_risk_model_features.json"

OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
OUTPUT_CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts" / "temporal_robustness"

ONE_YEAR_OUTPUT_PATH = OUTPUT_TABLES_DIR / "temporal_robustness_one_year.csv"
EXPANDING_OUTPUT_PATH = OUTPUT_TABLES_DIR / "temporal_robustness_expanding_holdout.csv"
OFFICIAL_OUTPUT_PATH = OUTPUT_TABLES_DIR / "temporal_robustness_official_split.csv"
SUMMARY_OUTPUT_PATH = OUTPUT_TABLES_DIR / "temporal_robustness_summary.json"

TARGET_COLUMN = "target_conflict_next_year"
PERSISTENCE_COLUMN = "organized_violence_exists"
OFFICIAL_TRAIN_END_YEAR = 2016
OFFICIAL_TEST_START_YEAR = 2017
OFFICIAL_TEST_END_YEAR = 2023


@dataclass(frozen=True)
class EvaluationWindow:
    scheme: str
    cutoff_year: int
    test_start_year: int
    test_end_year: int


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


def load_feature_columns() -> list[str]:
    metadata = json.loads(FEATURES_PATH.read_text(encoding="utf-8-sig"))
    feature_columns = metadata.get("feature_columns")
    if not isinstance(feature_columns, list) or not feature_columns:
        raise ValueError(f"Feature metadata does not contain a valid feature_columns list: {FEATURES_PATH}")
    return [str(column) for column in feature_columns]


def require_columns(df: pd.DataFrame, columns: Iterable[str]) -> None:
    missing_columns = [column for column in columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def safe_probability_metric(metric_name: str, y_true: pd.Series, y_proba: pd.Series) -> float | None:
    if y_true.nunique(dropna=False) < 2 and metric_name in {"roc_auc", "log_loss"}:
        return None

    try:
        if metric_name == "roc_auc":
            return float(roc_auc_score(y_true, y_proba))
        if metric_name == "average_precision":
            return float(average_precision_score(y_true, y_proba))
        if metric_name == "brier_score":
            return float(brier_score_loss(y_true, y_proba))
        if metric_name == "log_loss":
            return float(log_loss(y_true, y_proba, labels=[0, 1]))
    except ValueError:
        return None

    raise ValueError(f"Unsupported probability metric: {metric_name}")


def evaluate_binary_predictions(
    model_name: str,
    y_true: pd.Series,
    y_pred: pd.Series,
    y_proba: pd.Series | None = None,
) -> dict[str, float | int | str | None]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    row: dict[str, float | int | str | None] = {
        "model": model_name,
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_true, y_pred, zero_division=0)),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
        "predicted_positive_rate": float(pd.Series(y_pred).mean()),
        "actual_positive_rate": float(pd.Series(y_true).mean()),
        "roc_auc": None,
        "average_precision": None,
        "brier_score": None,
        "log_loss": None,
    }

    if y_proba is not None:
        row["roc_auc"] = safe_probability_metric("roc_auc", y_true, y_proba)
        row["average_precision"] = safe_probability_metric("average_precision", y_true, y_proba)
        row["brier_score"] = safe_probability_metric("brier_score", y_true, y_proba)
        row["log_loss"] = safe_probability_metric("log_loss", y_true, y_proba)

    return row


def evaluate_window(
    df: pd.DataFrame,
    feature_columns: list[str],
    window: EvaluationWindow,
) -> list[dict[str, float | int | str | None]]:
    train_mask = df["year"] <= window.cutoff_year
    test_mask = (df["year"] >= window.test_start_year) & (df["year"] <= window.test_end_year)

    X_train = df.loc[train_mask, feature_columns]
    y_train = df.loc[train_mask, TARGET_COLUMN]
    X_test = df.loc[test_mask, feature_columns]
    y_test = df.loc[test_mask, TARGET_COLUMN]

    if X_train.empty:
        raise ValueError(f"No training rows for {window}")
    if X_test.empty:
        raise ValueError(f"No test rows for {window}")
    if y_train.nunique(dropna=False) < 2:
        raise ValueError(f"Training target has fewer than two classes for {window}")

    model = build_model()
    model.fit(X_train, y_train)

    y_pred_model = pd.Series(model.predict(X_test), index=X_test.index)
    y_proba_model = pd.Series(model.predict_proba(X_test)[:, 1], index=X_test.index)
    y_pred_persistence = df.loc[test_mask, PERSISTENCE_COLUMN]

    baseline_row = evaluate_binary_predictions(
        model_name="Persistence baseline",
        y_true=y_test,
        y_pred=y_pred_persistence,
    )
    model_row = evaluate_binary_predictions(
        model_name="Logistic Regression scaled - World Bank all raw",
        y_true=y_test,
        y_pred=y_pred_model,
        y_proba=y_proba_model,
    )

    baseline_f1 = float(baseline_row["f1_score"])
    for row in (baseline_row, model_row):
        row.update(
            {
                "scheme": window.scheme,
                "cutoff_year": window.cutoff_year,
                "train_start_year": int(df.loc[train_mask, "year"].min()),
                "train_end_year": int(df.loc[train_mask, "year"].max()),
                "test_start_year": window.test_start_year,
                "test_end_year": window.test_end_year,
                "train_rows": int(train_mask.sum()),
                "test_rows": int(test_mask.sum()),
                "f1_difference_vs_persistence": float(row["f1_score"]) - baseline_f1,
            }
        )

    return [baseline_row, model_row]


def make_windows() -> tuple[list[EvaluationWindow], list[EvaluationWindow], list[EvaluationWindow]]:
    one_year_windows = [
        EvaluationWindow(
            scheme="rolling_one_year",
            cutoff_year=cutoff_year,
            test_start_year=cutoff_year + 1,
            test_end_year=cutoff_year + 1,
        )
        for cutoff_year in range(2012, 2023)
    ]

    expanding_windows = [
        EvaluationWindow(
            scheme="expanding_holdout",
            cutoff_year=cutoff_year,
            test_start_year=cutoff_year + 1,
            test_end_year=OFFICIAL_TEST_END_YEAR,
        )
        for cutoff_year in range(2012, 2019)
    ]

    official_windows = [
        EvaluationWindow(
            scheme="official_split_reproduction",
            cutoff_year=OFFICIAL_TRAIN_END_YEAR,
            test_start_year=OFFICIAL_TEST_START_YEAR,
            test_end_year=OFFICIAL_TEST_END_YEAR,
        )
    ]

    return one_year_windows, expanding_windows, official_windows


def evaluate_windows(
    df: pd.DataFrame,
    feature_columns: list[str],
    windows: list[EvaluationWindow],
) -> pd.DataFrame:
    rows: list[dict[str, float | int | str | None]] = []
    for window in windows:
        print(
            "[RUN] "
            f"{window.scheme}: train <= {window.cutoff_year}, "
            f"test {window.test_start_year}-{window.test_end_year}"
        )
        rows.extend(evaluate_window(df, feature_columns, window))

    columns = [
        "scheme",
        "model",
        "cutoff_year",
        "train_start_year",
        "train_end_year",
        "test_start_year",
        "test_end_year",
        "train_rows",
        "test_rows",
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "tn",
        "fp",
        "fn",
        "tp",
        "predicted_positive_rate",
        "actual_positive_rate",
        "roc_auc",
        "average_precision",
        "brier_score",
        "log_loss",
        "f1_difference_vs_persistence",
    ]

    return pd.DataFrame(rows)[columns]


def model_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["model"] == "Logistic Regression scaled - World Bank all raw"].copy()


def save_plot(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    print(f"[OK] Saved chart: {path.relative_to(PROJECT_ROOT)}")


def plot_one_year_charts(one_year_df: pd.DataFrame) -> None:
    model_df = model_rows(one_year_df)

    plt.figure(figsize=(9, 4.8))
    plt.plot(model_df["test_start_year"], model_df["f1_score"], marker="o", label="Logistic Regression")
    baseline_df = one_year_df[one_year_df["model"] == "Persistence baseline"]
    plt.plot(baseline_df["test_start_year"], baseline_df["f1_score"], marker="o", label="Persistence baseline")
    plt.title("F1 by one-year temporal test window")
    plt.xlabel("Test year")
    plt.ylabel("F1-score")
    plt.ylim(0, 1)
    plt.grid(alpha=0.25)
    plt.legend()
    save_plot(OUTPUT_CHARTS_DIR / "f1_by_test_year.png")

    plt.figure(figsize=(9, 4.8))
    plt.axhline(0, color="black", linewidth=1)
    plt.bar(model_df["test_start_year"], model_df["f1_difference_vs_persistence"])
    plt.title("F1 gain vs persistence baseline by test year")
    plt.xlabel("Test year")
    plt.ylabel("F1 difference")
    plt.grid(axis="y", alpha=0.25)
    save_plot(OUTPUT_CHARTS_DIR / "f1_gain_vs_persistence_by_year.png")

    plt.figure(figsize=(9, 4.8))
    plt.plot(model_df["test_start_year"], model_df["precision"], marker="o", label="Precision")
    plt.plot(model_df["test_start_year"], model_df["recall"], marker="o", label="Recall")
    plt.title("Precision and recall by one-year temporal test window")
    plt.xlabel("Test year")
    plt.ylabel("Score")
    plt.ylim(0, 1)
    plt.grid(alpha=0.25)
    plt.legend()
    save_plot(OUTPUT_CHARTS_DIR / "precision_recall_by_year.png")

    if model_df["brier_score"].notna().any():
        plt.figure(figsize=(9, 4.8))
        plt.plot(model_df["test_start_year"], model_df["brier_score"], marker="o")
        plt.title("Brier score by one-year temporal test window")
        plt.xlabel("Test year")
        plt.ylabel("Brier score")
        plt.grid(alpha=0.25)
        save_plot(OUTPUT_CHARTS_DIR / "brier_score_by_year.png")


def plot_expanding_chart(expanding_df: pd.DataFrame) -> None:
    model_df = model_rows(expanding_df)
    baseline_df = expanding_df[expanding_df["model"] == "Persistence baseline"]

    plt.figure(figsize=(9, 4.8))
    plt.plot(model_df["cutoff_year"], model_df["f1_score"], marker="o", label="Logistic Regression")
    plt.plot(baseline_df["cutoff_year"], baseline_df["f1_score"], marker="o", label="Persistence baseline")
    plt.title("F1 in expanding multi-year holdout")
    plt.xlabel("Training cutoff year")
    plt.ylabel("F1-score")
    plt.ylim(0, 1)
    plt.grid(alpha=0.25)
    plt.legend()
    save_plot(OUTPUT_CHARTS_DIR / "expanding_holdout_f1.png")


def finite_or_none(value: float | int | None) -> float | int | None:
    if value is None:
        return None
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def build_summary(
    one_year_df: pd.DataFrame,
    expanding_df: pd.DataFrame,
    official_df: pd.DataFrame,
    feature_columns: list[str],
) -> dict[str, object]:
    one_year_model = model_rows(one_year_df)
    expanding_model = model_rows(expanding_df)
    official_model = model_rows(official_df).iloc[0]
    official_baseline = official_df[official_df["model"] == "Persistence baseline"].iloc[0]

    one_year_wins = int((one_year_model["f1_difference_vs_persistence"] > 0).sum())
    one_year_ties = int((one_year_model["f1_difference_vs_persistence"] == 0).sum())
    one_year_losses = int((one_year_model["f1_difference_vs_persistence"] < 0).sum())

    expanding_wins = int((expanding_model["f1_difference_vs_persistence"] > 0).sum())
    expanding_ties = int((expanding_model["f1_difference_vs_persistence"] == 0).sum())
    expanding_losses = int((expanding_model["f1_difference_vs_persistence"] < 0).sum())

    return {
        "dataset": str(DATA_PATH.relative_to(PROJECT_ROOT)),
        "feature_metadata": str(FEATURES_PATH.relative_to(PROJECT_ROOT)),
        "n_features": len(feature_columns),
        "target_column": TARGET_COLUMN,
        "persistence_column": PERSISTENCE_COLUMN,
        "model": "Pipeline(SimpleImputer median -> StandardScaler -> LogisticRegression balanced)",
        "official_split": {
            "train_end_year": OFFICIAL_TRAIN_END_YEAR,
            "test_start_year": OFFICIAL_TEST_START_YEAR,
            "test_end_year": OFFICIAL_TEST_END_YEAR,
            "model_f1": finite_or_none(float(official_model["f1_score"])),
            "persistence_f1": finite_or_none(float(official_baseline["f1_score"])),
            "f1_difference_vs_persistence": finite_or_none(
                float(official_model["f1_difference_vs_persistence"])
            ),
            "model_accuracy": finite_or_none(float(official_model["accuracy"])),
            "model_precision": finite_or_none(float(official_model["precision"])),
            "model_recall": finite_or_none(float(official_model["recall"])),
            "model_brier_score": finite_or_none(float(official_model["brier_score"])),
            "model_roc_auc": finite_or_none(float(official_model["roc_auc"])),
            "model_average_precision": finite_or_none(float(official_model["average_precision"])),
        },
        "rolling_one_year": {
            "windows": int(len(one_year_model)),
            "wins_vs_persistence": one_year_wins,
            "ties_vs_persistence": one_year_ties,
            "losses_vs_persistence": one_year_losses,
            "mean_model_f1": finite_or_none(float(one_year_model["f1_score"].mean())),
            "mean_persistence_f1": finite_or_none(
                float(one_year_df[one_year_df["model"] == "Persistence baseline"]["f1_score"].mean())
            ),
            "mean_f1_difference_vs_persistence": finite_or_none(
                float(one_year_model["f1_difference_vs_persistence"].mean())
            ),
            "min_f1_difference_vs_persistence": finite_or_none(
                float(one_year_model["f1_difference_vs_persistence"].min())
            ),
            "max_f1_difference_vs_persistence": finite_or_none(
                float(one_year_model["f1_difference_vs_persistence"].max())
            ),
            "stable_win_vs_persistence": one_year_losses == 0 and one_year_ties == 0,
        },
        "expanding_holdout": {
            "windows": int(len(expanding_model)),
            "wins_vs_persistence": expanding_wins,
            "ties_vs_persistence": expanding_ties,
            "losses_vs_persistence": expanding_losses,
            "mean_model_f1": finite_or_none(float(expanding_model["f1_score"].mean())),
            "mean_persistence_f1": finite_or_none(
                float(expanding_df[expanding_df["model"] == "Persistence baseline"]["f1_score"].mean())
            ),
            "mean_f1_difference_vs_persistence": finite_or_none(
                float(expanding_model["f1_difference_vs_persistence"].mean())
            ),
            "min_f1_difference_vs_persistence": finite_or_none(
                float(expanding_model["f1_difference_vs_persistence"].min())
            ),
            "max_f1_difference_vs_persistence": finite_or_none(
                float(expanding_model["f1_difference_vs_persistence"].max())
            ),
            "stable_win_vs_persistence": expanding_losses == 0 and expanding_ties == 0,
        },
        "interpretation": (
            "The model is considered temporally stable only if it beats the persistence baseline "
            "in every rolling one-year and expanding holdout window."
        ),
    }


def validate_outputs() -> None:
    required_outputs = [
        ONE_YEAR_OUTPUT_PATH,
        EXPANDING_OUTPUT_PATH,
        OFFICIAL_OUTPUT_PATH,
        SUMMARY_OUTPUT_PATH,
        OUTPUT_CHARTS_DIR / "f1_by_test_year.png",
        OUTPUT_CHARTS_DIR / "f1_gain_vs_persistence_by_year.png",
        OUTPUT_CHARTS_DIR / "precision_recall_by_year.png",
        OUTPUT_CHARTS_DIR / "expanding_holdout_f1.png",
    ]

    missing = [path for path in required_outputs if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required temporal robustness outputs: {missing}")


def main() -> int:
    print("Temporal robustness evaluation")
    print("------------------------------")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Input dataset: {DATA_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Feature metadata: {FEATURES_PATH.relative_to(PROJECT_ROOT)}")

    OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    feature_columns = load_feature_columns()

    require_columns(
        df,
        ["year", TARGET_COLUMN, PERSISTENCE_COLUMN, *feature_columns],
    )

    print(f"Rows: {len(df)}")
    print(f"Year range: {int(df['year'].min())}-{int(df['year'].max())}")
    print(f"Features: {len(feature_columns)}")

    one_year_windows, expanding_windows, official_windows = make_windows()

    one_year_df = evaluate_windows(df, feature_columns, one_year_windows)
    expanding_df = evaluate_windows(df, feature_columns, expanding_windows)
    official_df = evaluate_windows(df, feature_columns, official_windows)

    one_year_df.to_csv(ONE_YEAR_OUTPUT_PATH, index=False)
    expanding_df.to_csv(EXPANDING_OUTPUT_PATH, index=False)
    official_df.to_csv(OFFICIAL_OUTPUT_PATH, index=False)
    print(f"[OK] Saved table: {ONE_YEAR_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"[OK] Saved table: {EXPANDING_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"[OK] Saved table: {OFFICIAL_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")

    plot_one_year_charts(one_year_df)
    plot_expanding_chart(expanding_df)

    summary = build_summary(one_year_df, expanding_df, official_df, feature_columns)
    SUMMARY_OUTPUT_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] Saved summary: {SUMMARY_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")

    validate_outputs()

    official = summary["official_split"]
    rolling = summary["rolling_one_year"]
    expanding = summary["expanding_holdout"]
    print()
    print("Summary:")
    print(
        "  Official split F1: "
        f"model={official['model_f1']:.4f}, "
        f"persistence={official['persistence_f1']:.4f}, "
        f"diff={official['f1_difference_vs_persistence']:.4f}"
    )
    print(
        "  Rolling one-year wins/ties/losses vs persistence: "
        f"{rolling['wins_vs_persistence']}/"
        f"{rolling['ties_vs_persistence']}/"
        f"{rolling['losses_vs_persistence']}"
    )
    print(
        "  Expanding holdout wins/ties/losses vs persistence: "
        f"{expanding['wins_vs_persistence']}/"
        f"{expanding['ties_vs_persistence']}/"
        f"{expanding['losses_vs_persistence']}"
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Temporal robustness evaluation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
