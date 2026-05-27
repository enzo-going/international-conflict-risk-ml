from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PRIO_PATH    = PROJECT_ROOT / "data" / "raw" / "ucdp" / "UcdpPrioConflict_v25_1.csv"
MAPPING_PATH = PROJECT_ROOT / "data" / "interim" / "country_name_mapping_reviewed.csv"
BASE_PATH    = PROJECT_ROOT / "data" / "final" / "conflict_country_year_base.csv"
OUTPUT_PATH  = PROJECT_ROOT / "data" / "intermediate" / "prio_country_year_base.csv"


def load_prio() -> pd.DataFrame:
    """Load the UCDP/PRIO Armed Conflict Dataset raw file."""
    if not PRIO_PATH.exists():
        raise FileNotFoundError(f"PRIO dataset not found: {PRIO_PATH}")
    return pd.read_csv(PRIO_PATH)


def load_mapping() -> pd.DataFrame:
    """Load the reviewed country name mapping."""
    if not MAPPING_PATH.exists():
        raise FileNotFoundError(f"Mapping file not found: {MAPPING_PATH}")
    return pd.read_csv(MAPPING_PATH)


def load_base_countries() -> set:
    """Load the set of standardized country names from the base dataset."""
    if not BASE_PATH.exists():
        raise FileNotFoundError(f"Base dataset not found: {BASE_PATH}")
    df = pd.read_csv(BASE_PATH, usecols=["country"])
    return set(df["country"].dropna().str.strip().str.title().unique())


def expand_multi_country_conflicts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expand rows where gwno_loc contains multiple countries (comma-separated).

    Interstate conflicts (type=2) are the main source of multi-country rows.
    Each country gets its own row so per-country features can be computed correctly.
    Sort order is mandatory before any downstream shift/rolling to avoid
    cross-conflict data leakage.
    """
    df = df.copy()
    df["gwno_loc_list"] = df["gwno_loc"].astype(str).str.split(",")
    df = df.explode("gwno_loc_list")
    df["gwno_loc_clean"] = df["gwno_loc_list"].str.strip().astype(int)
    df = df.drop(columns=["gwno_loc_list"])
    df = df.sort_values(["conflict_id", "gwno_loc_clean", "year"]).reset_index(drop=True)
    return df


def map_location_to_country(df: pd.DataFrame, df_mapping: pd.DataFrame,
                             base_countries: set) -> pd.DataFrame:
    """
    Map PRIO location names to the standardized country name used in the base dataset.

    Strategy
    --------
    1. Filter mapping to approved rows only (include_in_merge flag).
    2. Build ucdp_country → ucdp_normalized dict and apply via the location field.
    3. If coverage is below 80%, fall back to direct location matching against
       the known country names in the base dataset.

    Rows with no resolved country are kept with country=NaN so the caller
    can report unmapped locations before dropping them.
    """
    df = df.copy()

    if "include_in_merge" in df_mapping.columns:
        approved = df_mapping["include_in_merge"].astype(str).str.lower()
        df_mapping = df_mapping[approved.isin(["true", "1", "yes", "x"])].copy()

    loc_to_normalized = dict(
        zip(
            df_mapping["ucdp_country"].astype(str).str.strip(),
            df_mapping["ucdp_normalized"].astype(str).str.strip(),
        )
    )

    df["country"] = (
        df["location"].astype(str).str.strip().map(loc_to_normalized).str.title()
    )

    coverage = df["country"].notna().mean() * 100

    if coverage < 80:
        direct_match = df["location"].astype(str).str.strip().isin(base_countries)
        if direct_match.mean() > 0.5:
            df["country"] = df["location"].astype(str).str.strip().str.title()
            df.loc[~df["country"].isin(base_countries), "country"] = None

    df["country"] = df["country"].str.title()
    return df


def report_unmapped(df: pd.DataFrame) -> None:
    """Print locations that could not be resolved to a base-dataset country name."""
    unmapped = (
        df[df["country"].isna()][["gwno_loc_clean", "location"]]
        .drop_duplicates()
        .sort_values("location")
    )
    if unmapped.empty:
        return
    print(f"[AVISO] {len(unmapped)} locais sem mapeamento:")
    print(unmapped.to_string(index=False))
    print()
    print("  Para corrigir: adicionar em country_name_mapping_reviewed.csv")
    print("  ucdp_country = nome acima | ucdp_normalized = nome do dataset base")
    print()


def prepare_prio(df_prio: pd.DataFrame, df_mapping: pd.DataFrame,
                 base_countries: set) -> pd.DataFrame:
    """
    Full preparation pipeline: expand → map → report → drop unmapped.

    Returns a clean conflict-level DataFrame with one row per
    conflict_id × country × year, ready for feature engineering.
    """
    df = expand_multi_country_conflicts(df_prio)
    df = map_location_to_country(df, df_mapping, base_countries)
    report_unmapped(df)
    df = df[df["country"].notna()].copy()
    return df


def save_intermediate(df: pd.DataFrame) -> None:
    """Save the prepared conflict-level dataset to the intermediate data directory."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")


def main() -> None:
    df_prio        = load_prio()
    df_mapping     = load_mapping()
    base_countries = load_base_countries()

    df_prepared = prepare_prio(df_prio, df_mapping, base_countries)
    save_intermediate(df_prepared)

    n_total  = len(expand_multi_country_conflicts(df_prio))
    n_mapped = len(df_prepared)

    print("PRIO dataset prepared successfully.")
    print(f"Input   : {PRIO_PATH}")
    print(f"Output  : {OUTPUT_PATH}")
    print(f"Rows (after expand) : {n_total}")
    print(f"Rows (mapped)       : {n_mapped}  ({100 * n_mapped / n_total:.1f}%)")
    print(f"Conflitos únicos    : {df_prepared['conflict_id'].nunique()}")
    print(f"Países únicos       : {df_prepared['country'].nunique()}")
    print(f"Anos cobertos       : {df_prepared['year'].min()} – {df_prepared['year'].max()}")


if __name__ == "__main__":
    main()
