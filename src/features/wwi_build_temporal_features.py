from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "final"
    / "conflict_escalation_dataset.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "final"
    / "conflict_ml_features.csv"
)


TARGET_COLUMN = "future_conflict_escalation"


REQUIRED_COLUMNS = [
    "conflict_id",
    "country",
    "year",
    "total_deaths",
    TARGET_COLUMN,
]


def load_dataset() -> pd.DataFrame:
    """Load supervised conflict dataset."""

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


def create_temporal_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create temporal conflict features.
    """

    dataset = df.copy()

    dataset = dataset.sort_values(
        ["conflict_id", "year"]
    ).reset_index(drop=True)

    grouped = dataset.groupby("conflict_id")

    # Previous year deaths
    dataset["previous_year_deaths"] = (
        grouped["total_deaths"]
        .shift(1)
    )

    # Death growth rate
    dataset["death_growth_rate"] = (
        (
            dataset["total_deaths"]
            - dataset["previous_year_deaths"]
        )
        / dataset["previous_year_deaths"]
    )

    # Rolling average deaths (3 years)
    dataset["rolling_mean_deaths_3y"] = (
        grouped["total_deaths"]
        .rolling(window=3, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

    # Rolling max deaths
    dataset["rolling_max_deaths_3y"] = (
        grouped["total_deaths"]
        .rolling(window=3, min_periods=1)
        .max()
        .reset_index(level=0, drop=True)
    )

    # Conflict duration
    dataset["conflict_duration_years"] = (
        grouped.cumcount() + 1
    )

    # Cumulative deaths
    dataset["cumulative_deaths"] = (
        grouped["total_deaths"]
        .cumsum()
    )

    # Temporal momentum
    dataset["conflict_momentum"] = (
        dataset["total_deaths"]
        - dataset["rolling_mean_deaths_3y"]
    )

    return dataset


def clean_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean feature dataset.
    """

    dataset = df.copy()

    numeric_columns = [
        "total_deaths",
        "previous_year_deaths",
        "death_growth_rate",
        "rolling_mean_deaths_3y",
        "rolling_max_deaths_3y",
        "conflict_duration_years",
        "cumulative_deaths",
        "conflict_momentum",
    ]

    for column in numeric_columns:
        dataset[column] = pd.to_numeric(
            dataset[column],
            errors="coerce",
        )

    dataset[numeric_columns] = (
        dataset[numeric_columns]
        .replace([float("inf"), -float("inf")], 0)
        .fillna(0)
    )

    return dataset


def save_dataset(df: pd.DataFrame) -> None:
    """Save feature-engineered dataset."""

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
    """Print feature engineering summary."""

    print("Conflict feature dataset built successfully.")

    print(f"Output: {OUTPUT_PATH}")

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print()
    print("Created features:")

    created_features = [
        "previous_year_deaths",
        "death_growth_rate",
        "rolling_mean_deaths_3y",
        "rolling_max_deaths_3y",
        "conflict_duration_years",
        "cumulative_deaths",
        "conflict_momentum",
    ]

    for feature in created_features:
        print(f"- {feature}")

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

    dataset = create_temporal_features(
        dataset
    )

    dataset = clean_features(dataset)

    save_dataset(dataset)

    print_summary(dataset)


if __name__ == "__main__":
    main()