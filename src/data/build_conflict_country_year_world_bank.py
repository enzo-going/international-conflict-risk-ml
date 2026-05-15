from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFLICT_PATH = PROJECT_ROOT / "data" / "final" / "conflict_country_year_temporal.csv"
WORLD_BANK_PATH = (
    PROJECT_ROOT / "data" / "processed" / "world_bank" / "world_bank_country_year_indicators.csv"
)
COUNTRY_MAPPING_PATH = PROJECT_ROOT / "data" / "interim" / "country_name_mapping_reviewed.csv"

OUTPUT_PATH = PROJECT_ROOT / "data" / "final" / "conflict_country_year_world_bank.csv"

WORLD_BANK_FEATURE_COLUMNS = [
    "population_total",
    "gdp_per_capita_current_usd",
    "gdp_growth_annual_pct",
    "inflation_consumer_prices_annual_pct",
    "unemployment_total_pct",
    "military_expenditure_pct_gdp",
]


def build_conflict_world_bank_dataset() -> pd.DataFrame:
    conflict = pd.read_csv(CONFLICT_PATH)
    world_bank = pd.read_csv(WORLD_BANK_PATH)
    mapping = pd.read_csv(COUNTRY_MAPPING_PATH)

    valid_mapping = mapping[mapping["include_in_merge"] == True].copy()

    valid_mapping = valid_mapping[
        [
            "ucdp_country",
            "world_bank_country_code",
            "world_bank_country_name",
            "review_status",
        ]
    ].copy()

    conflict = conflict.merge(
        valid_mapping,
        left_on="country",
        right_on="ucdp_country",
        how="left",
    )

    missing_mapping = (
        conflict.loc[conflict["world_bank_country_code"].isna(), "country"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    conflict = conflict[conflict["world_bank_country_code"].notna()].copy()

    wb_columns = [
        "country_code",
        "year",
        "world_bank_region",
        "world_bank_income_level",
    ] + WORLD_BANK_FEATURE_COLUMNS

    world_bank = world_bank[wb_columns].copy()

    merged = conflict.merge(
        world_bank,
        left_on=["world_bank_country_code", "year"],
        right_on=["country_code", "year"],
        how="left",
    )

    merged = merged.drop(columns=["ucdp_country", "country_code"])

    merged.attrs["missing_mapping"] = missing_mapping

    return merged


def print_validation_summary(df: pd.DataFrame) -> None:
    missing_mapping = df.attrs.get("missing_mapping", [])

    print("Conflict + World Bank dataset built successfully.")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Countries: {df['country'].nunique()}")
    print(f"Years: {df['year'].min()} - {df['year'].max()}")

    print()
    print("Countries excluded due to missing/invalid World Bank mapping:")
    if missing_mapping:
        for country in missing_mapping:
            print(f"- {country}")
    else:
        print("None")

    print()
    print("Target distribution:")
    print(df["target_conflict_next_year"].value_counts().sort_index())

    print()
    print("Missing values in World Bank features:")
    missing = (
        df[WORLD_BANK_FEATURE_COLUMNS]
        .isna()
        .mean()
        .sort_values(ascending=False)
        .mul(100)
        .round(2)
    )
    print(missing)

    duplicated_pairs = df.duplicated(["country", "year"]).sum()
    print()
    print(f"Duplicated country-year pairs: {duplicated_pairs}")


def main() -> None:
    df = build_conflict_world_bank_dataset()

    df.to_csv(OUTPUT_PATH, index=False)

    print_validation_summary(df)


if __name__ == "__main__":
    main()
