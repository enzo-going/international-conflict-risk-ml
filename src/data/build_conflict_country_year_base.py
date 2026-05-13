from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_INPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "ucdp_organized_violence_country_year.csv"
)

FINAL_OUTPUT_PATH = PROJECT_ROOT / "data" / "final" / "conflict_country_year_base.csv"


CONFLICT_FLAG_COLUMNS = [
    "state_based_conflict_exists",
    "non_state_conflict_exists",
    "one_sided_violence_exists",
]


def load_processed_dataset() -> pd.DataFrame:
    """Load the processed UCDP country-year dataset."""
    if not PROCESSED_INPUT_PATH.exists():
        raise FileNotFoundError(f"Processed dataset not found: {PROCESSED_INPUT_PATH}")

    return pd.read_csv(PROCESSED_INPUT_PATH)


def validate_required_columns(df: pd.DataFrame) -> None:
    """Validate required columns for target construction."""
    required_columns = ["country_id", "country", "year", *CONFLICT_FLAG_COLUMNS]
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def build_target_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Build the first final country-year dataset with next-year conflict target."""
    validate_required_columns(df)

    dataset = df.copy()

    dataset["organized_violence_exists"] = (
        dataset[CONFLICT_FLAG_COLUMNS].fillna(0).astype(int).max(axis=1)
    )

    dataset = dataset.sort_values(["country_id", "year"]).reset_index(drop=True)

    dataset["target_conflict_next_year"] = (
        dataset.groupby("country_id")["organized_violence_exists"].shift(-1)
    )

    # Last available year for each country has no next-year label.
    dataset = dataset.dropna(subset=["target_conflict_next_year"]).copy()
    dataset["target_conflict_next_year"] = dataset["target_conflict_next_year"].astype(int)

    return dataset


def save_final_dataset(df: pd.DataFrame) -> None:
    """Save final modeling dataset."""
    FINAL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(FINAL_OUTPUT_PATH, index=False, encoding="utf-8")


def main() -> None:
    processed_df = load_processed_dataset()
    final_df = build_target_dataset(processed_df)
    save_final_dataset(final_df)

    target_distribution = final_df["target_conflict_next_year"].value_counts().sort_index()

    print("Base conflict country-year dataset built successfully.")
    print(f"Input: {PROCESSED_INPUT_PATH}")
    print(f"Output: {FINAL_OUTPUT_PATH}")
    print(f"Rows: {final_df.shape[0]}")
    print(f"Columns: {final_df.shape[1]}")
    print("Target distribution:")
    print(target_distribution.to_string())


if __name__ == "__main__":
    main()

