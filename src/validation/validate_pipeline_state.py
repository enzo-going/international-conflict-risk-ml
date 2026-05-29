from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASETS = {
    "processed_ucdp": PROJECT_ROOT
    / "data"
    / "processed"
    / "ucdp_organized_violence_country_year.csv",
    "final_base": PROJECT_ROOT / "data" / "final" / "conflict_country_year_base.csv",
    "final_temporal": PROJECT_ROOT
    / "data"
    / "final"
    / "conflict_country_year_temporal.csv",
    "processed_world_bank": PROJECT_ROOT
    / "data"
    / "processed"
    / "world_bank"
    / "world_bank_country_year_indicators.csv",
    "final_world_bank": PROJECT_ROOT
    / "data"
    / "final"
    / "conflict_country_year_world_bank.csv",
    "final_world_bank_features": PROJECT_ROOT
    / "data"
    / "final"
    / "conflict_country_year_world_bank_features.csv",
}

FEATURE_METADATA_PATH = (
    PROJECT_ROOT / "outputs" / "models" / "conflict_risk_model_features.json"
)

WORLD_BANK_COLUMNS = [
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


class Audit:
    def __init__(self) -> None:
        self.pass_count = 0
        self.warn_count = 0
        self.fail_count = 0

    def pass_(self, message: str) -> None:
        self.pass_count += 1
        print(f"PASS {message}")

    def warn(self, message: str) -> None:
        self.warn_count += 1
        print(f"WARN {message}")

    def fail(self, message: str) -> None:
        self.fail_count += 1
        print(f"FAIL {message}")

    def summary(self) -> None:
        print()
        print("Summary")
        print(f"PASS: {self.pass_count}")
        print(f"WARN: {self.warn_count}")
        print(f"FAIL: {self.fail_count}")


def relpath(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT))


def read_dataset(name: str, path: Path, audit: Audit) -> pd.DataFrame | None:
    if not path.exists():
        audit.fail(f"{name}: missing file {relpath(path)}")
        return None

    try:
        df = pd.read_csv(path)
    except Exception as exc:
        audit.fail(f"{name}: could not read CSV {relpath(path)} ({exc})")
        return None

    audit.pass_(f"{name}: exists at {relpath(path)}")
    audit.pass_(f"{name}: shape rows={df.shape[0]} columns={df.shape[1]}")
    return df


def validate_years(name: str, df: pd.DataFrame, audit: Audit) -> None:
    if "year" not in df.columns:
        audit.warn(f"{name}: no year column found")
        return

    if df["year"].isna().all():
        audit.fail(f"{name}: year column is entirely missing")
        return

    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    audit.pass_(f"{name}: years covered {min_year}-{max_year}")


def validate_country_year_duplicates(name: str, df: pd.DataFrame, audit: Audit) -> None:
    key_candidates = [
        ("country", "year"),
        ("country_id", "year"),
        ("country_code", "year"),
    ]

    checked = False

    for key in key_candidates:
        if all(column in df.columns for column in key):
            checked = True
            duplicated = int(df.duplicated(list(key)).sum())
            key_name = "+".join(key)
            if duplicated == 0:
                audit.pass_(f"{name}: no duplicated rows by {key_name}")
            else:
                audit.fail(f"{name}: {duplicated} duplicated rows by {key_name}")

    if not checked:
        audit.warn(f"{name}: no country-year compatible key found")


def validate_target_distribution(name: str, df: pd.DataFrame, audit: Audit) -> None:
    target = "target_conflict_next_year"

    if target not in df.columns:
        audit.warn(f"{name}: no {target} column found")
        return

    distribution = df[target].value_counts(dropna=False).sort_index()
    formatted = ", ".join(f"{key}={value}" for key, value in distribution.items())
    audit.pass_(f"{name}: target distribution {formatted}")

    if df[target].isna().any():
        audit.fail(f"{name}: target contains missing values")


def validate_world_bank_merge(
    temporal_df: pd.DataFrame | None,
    world_bank_df: pd.DataFrame | None,
    audit: Audit,
) -> None:
    if temporal_df is None or world_bank_df is None:
        audit.fail("world_bank_merge: cannot validate row loss because required datasets are missing")
        return

    row_loss = len(temporal_df) - len(world_bank_df)
    country_loss = temporal_df["country"].nunique() - world_bank_df["country"].nunique()

    if row_loss == 0:
        audit.pass_("world_bank_merge: no row loss from temporal to World Bank dataset")
    else:
        audit.warn(f"world_bank_merge: row loss from temporal to World Bank dataset = {row_loss}")

    if country_loss == 0:
        audit.pass_("world_bank_merge: no country loss from temporal to World Bank dataset")
    else:
        audit.warn(
            f"world_bank_merge: country loss from temporal to World Bank dataset = {country_loss}"
        )

    removed_countries = sorted(set(temporal_df["country"]) - set(world_bank_df["country"]))

    if removed_countries:
        audit.warn("world_bank_merge: removed countries = " + ", ".join(removed_countries))
    else:
        audit.pass_("world_bank_merge: no removed countries detected")


def validate_world_bank_nulls(df: pd.DataFrame | None, audit: Audit) -> None:
    if df is None:
        audit.fail("world_bank_nulls: cannot validate because final World Bank dataset is missing")
        return

    missing_columns = [column for column in WORLD_BANK_COLUMNS if column not in df.columns]

    if missing_columns:
        audit.fail("world_bank_nulls: missing columns = " + ", ".join(missing_columns))
        return

    null_rates = df[WORLD_BANK_COLUMNS].isna().mean().mul(100).sort_values(ascending=False)

    print()
    print("World Bank null percentages")

    for column, percent in null_rates.items():
        message = f"{column}: {percent:.2f}% null"
        if percent >= 20:
            audit.warn(message)
        else:
            audit.pass_(message)


def read_feature_metadata(audit: Audit) -> dict[str, Any] | None:
    if not FEATURE_METADATA_PATH.exists():
        audit.warn(f"feature_metadata: missing file {relpath(FEATURE_METADATA_PATH)}")
        return None

    try:
        metadata = json.loads(FEATURE_METADATA_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        audit.fail(f"feature_metadata: could not read JSON ({exc})")
        return None

    audit.pass_(f"feature_metadata: exists at {relpath(FEATURE_METADATA_PATH)}")
    return metadata


def validate_feature_metadata(
    df: pd.DataFrame | None,
    metadata: dict[str, Any] | None,
    audit: Audit,
) -> None:
    if metadata is None:
        return

    if df is None:
        audit.fail("feature_metadata: cannot validate because final feature dataset is missing")
        return

    feature_columns = metadata.get("feature_columns")

    if not isinstance(feature_columns, list):
        audit.fail("feature_metadata: feature_columns is missing or is not a list")
        return

    missing_from_dataset = [column for column in feature_columns if column not in df.columns]

    if missing_from_dataset:
        audit.fail(
            "feature_metadata: columns missing from final dataset = "
            + ", ".join(missing_from_dataset)
        )
    else:
        audit.pass_("feature_metadata: all listed features exist in final dataset")

    n_features = metadata.get("n_features")

    if n_features == len(feature_columns):
        audit.pass_(f"feature_metadata: n_features matches feature_columns ({len(feature_columns)})")
    else:
        audit.warn(
            f"feature_metadata: n_features={n_features} but feature_columns={len(feature_columns)}"
        )


def main() -> None:
    audit = Audit()
    datasets: dict[str, pd.DataFrame | None] = {}

    print("Pipeline state audit")
    print(f"Project root: {PROJECT_ROOT}")
    print()

    for name, path in DATASETS.items():
        df = read_dataset(name, path, audit)
        datasets[name] = df

        if df is None:
            continue

        validate_years(name, df, audit)
        validate_country_year_duplicates(name, df, audit)
        validate_target_distribution(name, df, audit)
        print()

    validate_world_bank_merge(
        temporal_df=datasets["final_temporal"],
        world_bank_df=datasets["final_world_bank"],
        audit=audit,
    )

    validate_world_bank_nulls(datasets["final_world_bank"], audit)

    metadata = read_feature_metadata(audit)
    validate_feature_metadata(datasets["final_world_bank_features"], metadata, audit)

    audit.summary()


if __name__ == "__main__":
    main()
