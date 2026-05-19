from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "world_war_1_details_clean.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "final"
    / "conflict_escalation_dataset.csv"
)


REQUIRED_COLUMNS = [
    "conflict_id",
    "country",
    "year",
    "total_deaths",
]


TARGET_COLUMN = "future_conflict_escalation"


def load_dataset() -> pd.DataFrame:
    """Load processed conflict dataset."""

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_PATH}"
        )

    return pd.read_csv(INPUT_PATH)


def validate_columns(df: pd.DataFrame) -> None:
    """Validate required columns."""

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


def create_future_conflict_target(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create future conflict escalation target.

    1 = future conflict intensity increased
    0 = future conflict intensity decreased or remained stable
    """

    dataset = df.copy()

    dataset = dataset.sort_values(
        ["conflict_id", "year"]
    ).reset_index(drop=True)

    dataset["next_year_deaths"] = (
        dataset
        .groupby("conflict_id")["total_deaths"]
        .shift(-1)
    )

    dataset = dataset.dropna(
        subset=["next_year_deaths"]
    ).copy()

    dataset[TARGET_COLUMN] = (
        dataset["next_year_deaths"]
        > dataset["total_deaths"]
    ).astype(int)

    return dataset


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare ML features.
    """

    dataset = df.copy()

    numeric_columns = [
        "total_deaths",
    ]

    for column in numeric_columns:
        dataset[column] = pd.to_numeric(
            dataset[column],
            errors="coerce",
        )

    dataset[numeric_columns] = (
        dataset[numeric_columns]
        .fillna(0)
    )

    return dataset


def save_dataset(df: pd.DataFrame) -> None:
    """Save final supervised dataset."""

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8",
    )


def print_summary(df: pd.DataFrame) -> None:
    """Print dataset summary."""

    print("Conflict escalation dataset built successfully.")

    print(f"Output: {OUTPUT_PATH}")

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print()
    print("Target distribution:")

    print(
        df[TARGET_COLUMN]
        .value_counts()
        .sort_index()
    )


def main() -> None:
    dataset = load_dataset()

    validate_columns(dataset)

    dataset = prepare_features(dataset)

    dataset = create_future_conflict_target(dataset)

    save_dataset(dataset)

    print_summary(dataset)


if __name__ == "__main__":
    main()