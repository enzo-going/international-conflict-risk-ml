from __future__ import annotations

import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"
DATABASE_PATH = PROJECT_ROOT / "data" / "database" / "conflict_risk_ml.sqlite"

FEATURES_PATH = PROJECT_ROOT / "data" / "final" / "conflict_country_year_world_bank_features.csv"
PREDICTIONS_PATH = PROJECT_ROOT / "outputs" / "tables" / "conflict_risk_model_test_predictions.csv"
METRICS_PATH = PROJECT_ROOT / "outputs" / "tables" / "conflict_risk_model_metrics.csv"
COEFFICIENTS_PATH = PROJECT_ROOT / "outputs" / "tables" / "conflict_risk_model_coefficients.csv"
CANDIDATE_MODELS_PATH = PROJECT_ROOT / "outputs" / "tables" / "candidate_model_comparison.csv"


def get_git_commit_hash() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Required input file not found: {path}")

    return pd.read_csv(path)


def get_table_columns(connection: sqlite3.Connection, table_name: str) -> list[str]:
    rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [row[1] for row in rows]


def align_to_table_schema(
    df: pd.DataFrame,
    connection: sqlite3.Connection,
    table_name: str,
) -> pd.DataFrame:
    table_columns = get_table_columns(connection, table_name)

    missing_columns = [column for column in table_columns if column not in df.columns]

    for column in missing_columns:
        df[column] = None

    return df[table_columns]


def rename_prediction_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_candidates = {
        "y_true": [
            "y_true",
            "target_conflict_next_year",
            "actual",
            "true_label",
        ],
        "y_pred": [
            "y_pred",
            "y_pred_model",
            "prediction",
            "predicted_label",
            "predicted_conflict_next_year",
        ],
        "y_proba": [
            "y_proba",
            "y_proba_model",
            "probability",
            "predicted_probability",
            "predicted_risk",
            "predicted_conflict_probability",
        ],
    }

    rename_map: dict[str, str] = {}

    for target_column, possible_names in rename_candidates.items():
        for name in possible_names:
            if name in df.columns:
                rename_map[name] = target_column
                break

    return df.rename(columns=rename_map)


def validate_required_columns(df: pd.DataFrame, required_columns: list[str], context: str) -> None:
    missing = [column for column in required_columns if column not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns in {context}: {missing}")


def load_country_year_features(connection: sqlite3.Connection) -> int:
    df = read_csv(FEATURES_PATH)

    validate_required_columns(
        df,
        ["country", "year"],
        "country-year features dataset",
    )

    df = align_to_table_schema(df, connection, "country_year_features")

    df.to_sql(
        "country_year_features",
        connection,
        if_exists="append",
        index=False,
    )

    return len(df)


def load_model_predictions(connection: sqlite3.Connection) -> int:
    predictions_df = read_csv(PREDICTIONS_PATH)
    predictions_df = rename_prediction_columns(predictions_df)

    validate_required_columns(
        predictions_df,
        ["country", "year"],
        "model predictions dataset",
    )

    features_df = read_csv(FEATURES_PATH)

    if "organized_violence_exists" not in predictions_df.columns:
        predictions_df = predictions_df.merge(
            features_df[["country", "year", "organized_violence_exists"]],
            on=["country", "year"],
            how="left",
        )

    predictions_df = align_to_table_schema(
        predictions_df,
        connection,
        "model_predictions",
    )

    predictions_df.to_sql(
        "model_predictions",
        connection,
        if_exists="append",
        index=False,
    )

    return len(predictions_df)


def load_model_metrics(connection: sqlite3.Connection) -> int:
    df = read_csv(METRICS_PATH)

    validate_required_columns(
        df,
        ["model", "accuracy", "precision", "recall", "f1_score"],
        "model metrics dataset",
    )

    df = align_to_table_schema(df, connection, "model_metrics")

    df.to_sql(
        "model_metrics",
        connection,
        if_exists="append",
        index=False,
    )

    return len(df)


def load_model_coefficients(connection: sqlite3.Connection) -> int:
    df = read_csv(COEFFICIENTS_PATH)

    validate_required_columns(
        df,
        [
            "rank",
            "feature",
            "feature_group",
            "coefficient",
            "absolute_coefficient",
            "effect",
        ],
        "model coefficients dataset",
    )

    df = align_to_table_schema(df, connection, "model_coefficients")

    df.to_sql(
        "model_coefficients",
        connection,
        if_exists="append",
        index=False,
    )

    return len(df)



def load_candidate_model_comparison(connection: sqlite3.Connection) -> int:
    df = read_csv(CANDIDATE_MODELS_PATH)

    validate_required_columns(
        df,
        [
            "model",
            "feature_count",
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "tn",
            "fp",
            "fn",
            "tp",
            "f1_difference_vs_persistence",
        ],
        "candidate model comparison dataset",
    )

    df = align_to_table_schema(df, connection, "candidate_model_comparison")

    df.to_sql(
        "candidate_model_comparison",
        connection,
        if_exists="append",
        index=False,
    )

    return len(df)


def insert_metadata(connection: sqlite3.Connection, rows_loaded: dict[str, int]) -> None:
    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": get_git_commit_hash(),
        "database_path": str(DATABASE_PATH.relative_to(PROJECT_ROOT)),
        "schema_path": str(SCHEMA_PATH.relative_to(PROJECT_ROOT)),
        "features_source": str(FEATURES_PATH.relative_to(PROJECT_ROOT)),
        "predictions_source": str(PREDICTIONS_PATH.relative_to(PROJECT_ROOT)),
        "metrics_source": str(METRICS_PATH.relative_to(PROJECT_ROOT)),
        "coefficients_source": str(COEFFICIENTS_PATH.relative_to(PROJECT_ROOT)),
        "candidate_models_source": str(CANDIDATE_MODELS_PATH.relative_to(PROJECT_ROOT)),
    }

    for table_name, row_count in rows_loaded.items():
        metadata[f"{table_name}_rows"] = str(row_count)

    metadata_df = pd.DataFrame(
        [{"key": key, "value": value} for key, value in metadata.items()]
    )

    metadata_df.to_sql(
        "dataset_metadata",
        connection,
        if_exists="append",
        index=False,
    )


def validate_database(connection: sqlite3.Connection) -> None:
    tables = [
        "country_year_features",
        "model_predictions",
        "model_coefficients",
        "model_metrics",
        "candidate_model_comparison",
        "dataset_metadata",
    ]

    print()
    print("SQLite validation:")

    for table in tables:
        count = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"- {table}: {count} rows")


def main() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.executescript(schema_sql)

        rows_loaded = {
            "country_year_features": load_country_year_features(connection),
            "model_predictions": load_model_predictions(connection),
            "model_metrics": load_model_metrics(connection),
            "model_coefficients": load_model_coefficients(connection),
            "candidate_model_comparison": load_candidate_model_comparison(connection),
        }

        insert_metadata(connection, rows_loaded)

        connection.commit()

        validate_database(connection)

    print()
    print("SQLite database generated successfully.")
    print(f"Output: {DATABASE_PATH}")


if __name__ == "__main__":
    main()