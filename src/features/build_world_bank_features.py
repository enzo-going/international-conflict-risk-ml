from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = PROJECT_ROOT / "data" / "final" / "conflict_country_year_world_bank.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "final" / "conflict_country_year_world_bank_features.csv"

WORLD_BANK_FEATURE_COLUMNS = [
    "population_total",
    "population_growth_annual_pct",
    "urban_population_pct",
    "gdp_per_capita_current_usd",
    "gdp_growth_annual_pct",
    "inflation_consumer_prices_annual_pct",
    "unemployment_total_pct",
    "school_enrollment_secondary_gross_pct",
    "military_expenditure_pct_gdp",
    "natural_resources_rents_pct_gdp",
]


def add_world_bank_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["country", "year"]).reset_index(drop=True)

    grouped = df.groupby("country", group_keys=False)

    for column in WORLD_BANK_FEATURE_COLUMNS:
        missing_column = f"{column}_missing"
        lag_column = f"{column}_lag1"
        change_column = f"{column}_change_1y"
        rolling_column = f"{column}_rolling_3y_mean"

        df[missing_column] = df[column].isna().astype(int)

        df[lag_column] = grouped[column].shift(1)

        df[change_column] = df[column] - df[lag_column]

        df[rolling_column] = grouped[column].transform(
            lambda series: series.rolling(window=3, min_periods=1).mean()
        )

    return df


def print_validation_summary(df: pd.DataFrame) -> None:
    derived_columns = [
        column
        for column in df.columns
        if (
            column.endswith("_missing")
            or column.endswith("_lag1")
            or column.endswith("_change_1y")
            or column.endswith("_rolling_3y_mean")
        )
    ]

    print("World Bank feature-engineered dataset built successfully.")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Countries: {df['country'].nunique()}")
    print(f"Years: {df['year'].min()} - {df['year'].max()}")

    print()
    print(f"New derived columns: {len(derived_columns)}")

    print()
    print("Missing values in derived lag/change/rolling columns:")
    missing = (
        df[derived_columns]
        .isna()
        .mean()
        .sort_values(ascending=False)
        .mul(100)
        .round(2)
    )

    print(missing.head(20))

    duplicated_pairs = df.duplicated(["country", "year"]).sum()

    print()
    print(f"Duplicated country-year pairs: {duplicated_pairs}")


def main() -> None:
    df = pd.read_csv(INPUT_PATH)

    df = add_world_bank_temporal_features(df)

    df.to_csv(OUTPUT_PATH, index=False)

    print_validation_summary(df)


if __name__ == "__main__":
    main()
