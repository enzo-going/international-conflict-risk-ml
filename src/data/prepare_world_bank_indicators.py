from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "world_bank"
PROCESSED_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "world_bank"

PROCESSED_OUTPUT_PATH = (
    PROCESSED_OUTPUT_DIR / "world_bank_country_year_indicators.csv"
)

START_YEAR = 1989
END_YEAR = 2023

INDICATORS = {
    "SP.POP.TOTL": "population_total",
    "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth_annual_pct",
    "FP.CPI.TOTL.ZG": "inflation_consumer_prices_annual_pct",
    "SL.UEM.TOTL.ZS": "unemployment_total_pct",
    "MS.MIL.XPND.GD.ZS": "military_expenditure_pct_gdp",
}


def request_json(url: str, timeout: int = 60) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "international-conflict-risk-ml/0.1"
        },
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8")

    return json.loads(raw)


def build_url(path: str, params: dict[str, str | int]) -> str:
    query = urllib.parse.urlencode(params)
    return f"https://api.worldbank.org/v2/{path}?{query}"


def fetch_world_bank_countries() -> pd.DataFrame:
    url = build_url(
        "country",
        {
            "format": "json",
            "per_page": 400,
        },
    )

    payload = request_json(url)

    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError("Unexpected country metadata response from World Bank API.")

    records = payload[1]

    countries = []

    for item in records:
        region = item.get("region") or {}
        income_level = item.get("incomeLevel") or {}

        country_code = item.get("id")
        iso2_code = item.get("iso2Code")
        country_name = item.get("name")
        region_name = region.get("value")
        income_level_name = income_level.get("value")

        is_aggregate = region_name == "Aggregates"

        countries.append(
            {
                "country_code": country_code,
                "iso2_code": iso2_code,
                "country_name": country_name,
                "world_bank_region": region_name,
                "world_bank_income_level": income_level_name,
                "is_aggregate": is_aggregate,
            }
        )

    df = pd.DataFrame(countries)

    df = df[
        (df["country_code"].notna())
        & (df["country_code"].str.len() == 3)
        & (~df["is_aggregate"])
    ].copy()

    return df.drop(columns=["is_aggregate"])


def fetch_indicator(indicator_code: str, feature_name: str) -> pd.DataFrame:
    url = build_url(
        f"country/all/indicator/{indicator_code}",
        {
            "format": "json",
            "per_page": 20000,
            "date": f"{START_YEAR}:{END_YEAR}",
        },
    )

    print(f"Downloading {indicator_code} -> {feature_name}")

    payload = request_json(url)

    raw_path = RAW_OUTPUT_DIR / f"{indicator_code}.json"
    raw_path.write_text(
        json.dumps(payload, ensure_ascii=False),
        encoding="utf-8",
    )

    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(f"Unexpected response for indicator {indicator_code}.")

    records = payload[1] or []

    rows = []

    for item in records:
        rows.append(
            {
                "country_code": item.get("countryiso3code"),
                "year": int(item.get("date")),
                feature_name: item.get("value"),
            }
        )

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError(f"No data returned for indicator {indicator_code}.")

    df = df[
        (df["country_code"].notna())
        & (df["country_code"].str.len() == 3)
    ].copy()

    df[feature_name] = pd.to_numeric(df[feature_name], errors="coerce")

    return df


def build_world_bank_country_year_dataset() -> pd.DataFrame:
    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    countries = fetch_world_bank_countries()

    output = countries.copy()

    years = pd.DataFrame({"year": list(range(START_YEAR, END_YEAR + 1))})

    output = output.merge(years, how="cross")

    for indicator_code, feature_name in INDICATORS.items():
        indicator_df = fetch_indicator(indicator_code, feature_name)

        output = output.merge(
            indicator_df[["country_code", "year", feature_name]],
            on=["country_code", "year"],
            how="left",
        )

        time.sleep(0.2)

    output = output.sort_values(["country_code", "year"]).reset_index(drop=True)

    return output


def print_validation_summary(df: pd.DataFrame) -> None:
    indicator_columns = list(INDICATORS.values())

    print("\nWorld Bank country-year dataset built successfully.")
    print(f"Output: {PROCESSED_OUTPUT_PATH}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Countries: {df['country_code'].nunique()}")
    print(f"Years: {df['year'].min()} - {df['year'].max()}")

    duplicated_pairs = df.duplicated(["country_code", "year"]).sum()
    print(f"Duplicated country-year pairs: {duplicated_pairs}")

    print("\nMissing values by indicator:")
    missing = (
        df[indicator_columns]
        .isna()
        .mean()
        .sort_values(ascending=False)
        .mul(100)
        .round(2)
    )

    print(missing)


def main() -> None:
    df = build_world_bank_country_year_dataset()

    df.to_csv(PROCESSED_OUTPUT_PATH, index=False)

    print_validation_summary(df)


if __name__ == "__main__":
    main()
