from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "ucdp" / "organizedviolencecy_v25_1.xlsx"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "ucdp_organized_violence_country_year.csv"


COLUMNS_TO_KEEP = [
    "country_id_cy",
    "country_cy",
    "year_cy",
    "region_cy",
    "main_govt_name_cy",
    "sb_exist_cy",
    "sb_dyad_count_cy",
    "sb_total_deaths_best_cy",
    "sb_intrastate_exist_cy",
    "sb_intrastate_deaths_best_cy",
    "sb_interstate_exist_cy",
    "sb_interstate_deaths_best_cy",
    "ns_exist_cy",
    "ns_dyad_count_cy",
    "ns_total_deaths_best_cy",
    "os_exist_cy",
    "os_dyad_count_cy",
    "os_total_deaths_best_cy",
    "cumulative_total_deaths_in_orgvio_best_cy",
    "version",
]


COLUMN_RENAME_MAP = {
    "country_id_cy": "country_id",
    "country_cy": "country",
    "year_cy": "year",
    "region_cy": "region",
    "main_govt_name_cy": "main_government_name",
    "sb_exist_cy": "state_based_conflict_exists",
    "sb_dyad_count_cy": "state_based_dyad_count",
    "sb_total_deaths_best_cy": "state_based_deaths_best",
    "sb_intrastate_exist_cy": "intrastate_conflict_exists",
    "sb_intrastate_deaths_best_cy": "intrastate_deaths_best",
    "sb_interstate_exist_cy": "interstate_conflict_exists",
    "sb_interstate_deaths_best_cy": "interstate_deaths_best",
    "ns_exist_cy": "non_state_conflict_exists",
    "ns_dyad_count_cy": "non_state_dyad_count",
    "ns_total_deaths_best_cy": "non_state_deaths_best",
    "os_exist_cy": "one_sided_violence_exists",
    "os_dyad_count_cy": "one_sided_dyad_count",
    "os_total_deaths_best_cy": "one_sided_deaths_best",
    "cumulative_total_deaths_in_orgvio_best_cy": "cumulative_organized_violence_deaths_best",
    "version": "ucdp_version",
}


def load_raw_dataset() -> pd.DataFrame:
    """Load the raw UCDP Organized Violence country-year Excel file."""
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw dataset not found: {RAW_PATH}")

    return pd.read_excel(RAW_PATH, sheet_name="Sheet1")


def validate_columns(df: pd.DataFrame) -> None:
    """Validate whether all required columns exist in the raw dataset."""
    missing_columns = [column for column in COLUMNS_TO_KEEP if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def prepare_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Select, rename and minimally validate the dataset."""
    validate_columns(df)

    processed = df[COLUMNS_TO_KEEP].copy()
    processed = processed.rename(columns=COLUMN_RENAME_MAP)

    processed["year"] = processed["year"].astype(int)

    duplicated_rows = processed.duplicated(subset=["country_id", "year"]).sum()

    if duplicated_rows > 0:
        raise ValueError(f"Found duplicated country-year rows: {duplicated_rows}")

    processed = processed.sort_values(["country", "year"]).reset_index(drop=True)

    return processed


def save_processed_dataset(df: pd.DataFrame) -> None:
    """Save the processed dataset as CSV."""
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False, encoding="utf-8")


def main() -> None:
    raw_df = load_raw_dataset()
    processed_df = prepare_dataset(raw_df)
    save_processed_dataset(processed_df)

    print("UCDP Organized Violence dataset processed successfully.")
    print(f"Input: {RAW_PATH}")
    print(f"Output: {PROCESSED_PATH}")
    print(f"Rows: {processed_df.shape[0]}")
    print(f"Columns: {processed_df.shape[1]}")
    print("Columns:")
    for column in processed_df.columns:
        print(f"- {column}")


if __name__ == "__main__":
    main()