from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = PROJECT_ROOT / "data" / "final" / "conflict_country_year_base.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "final" / "conflict_country_year_temporal.csv"


def load_dataset() -> pd.DataFrame:
    """Load the first final country-year dataset."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input dataset not found: {INPUT_PATH}")

    return pd.read_csv(INPUT_PATH)


def add_temporal_features(group: pd.DataFrame) -> pd.DataFrame:
    """Add temporal features for a single country."""
    group = group.sort_values("year").copy()

    conflict = group["organized_violence_exists"]
    deaths = group["state_based_deaths_best"] + group["non_state_deaths_best"] + group["one_sided_deaths_best"]

    group["conflict_previous_year"] = conflict.shift(1).fillna(0).astype(int)

    group["conflict_last_3_years_count"] = (
        conflict.shift(1).rolling(window=3, min_periods=1).sum().fillna(0).astype(int)
    )

    group["conflict_last_5_years_count"] = (
        conflict.shift(1).rolling(window=5, min_periods=1).sum().fillna(0).astype(int)
    )

    group["deaths_previous_year"] = deaths.shift(1).fillna(0)

    group["deaths_last_3_years_sum"] = (
        deaths.shift(1).rolling(window=3, min_periods=1).sum().fillna(0)
    )

    group["deaths_last_5_years_sum"] = (
        deaths.shift(1).rolling(window=5, min_periods=1).sum().fillna(0)
    )

    years_since_last_conflict = []
    last_conflict_year = None

    for _, row in group.iterrows():
        current_year = row["year"]

        if last_conflict_year is None:
            years_since_last_conflict.append(np.nan)
        else:
            years_since_last_conflict.append(current_year - last_conflict_year)

        if row["organized_violence_exists"] == 1:
            last_conflict_year = current_year

    group["years_since_last_conflict"] = years_since_last_conflict
    group["years_since_last_conflict"] = group["years_since_last_conflict"].fillna(999).astype(int)

    return group


def build_temporal_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Build conflict country-year dataset with temporal features."""
    required_columns = [
        "country_id",
        "country",
        "year",
        "organized_violence_exists",
        "state_based_deaths_best",
        "non_state_deaths_best",
        "one_sided_deaths_best",
        "target_conflict_next_year",
    ]

    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = df.sort_values(["country_id", "year"]).copy()

    temporal_df = (
        df.groupby("country_id", group_keys=False)
        .apply(add_temporal_features)
        .reset_index(drop=True)
    )

    return temporal_df


def save_dataset(df: pd.DataFrame) -> None:
    """Save the temporal-feature final dataset."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")


def main() -> None:
    df = load_dataset()
    temporal_df = build_temporal_dataset(df)
    save_dataset(temporal_df)

    new_columns = [
        "conflict_previous_year",
        "conflict_last_3_years_count",
        "conflict_last_5_years_count",
        "deaths_previous_year",
        "deaths_last_3_years_sum",
        "deaths_last_5_years_sum",
        "years_since_last_conflict",
    ]

    print("Temporal feature dataset built successfully.")
    print(f"Input: {INPUT_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Rows: {temporal_df.shape[0]}")
    print(f"Columns: {temporal_df.shape[1]}")
    print("New temporal features:")
    for column in new_columns:
        print(f"- {column}")


if __name__ == "__main__":
    main()
