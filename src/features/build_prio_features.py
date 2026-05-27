from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INTERMEDIATE_PATH = PROJECT_ROOT / "data" / "intermediate" / "prio_country_year_base.csv"
BASE_PATH         = PROJECT_ROOT / "data" / "final" / "conflict_country_year_base.csv"
OUTPUT_PATH       = PROJECT_ROOT / "data" / "final" / "conflict_country_year_prio.csv"

PRIO_FEATURE_COLS = [
    "prio_n_conflicts_active",
    "prio_max_intensity",
    "prio_max_intensity_trend",
    "prio_max_intensity_ma3",
    "prio_mean_intensity_ma3",
    "prio_mean_conflict_age",
    "prio_any_war_level",
    "prio_any_recurring",
    "prio_any_cumulative_war",
    "prio_sum_episode_duration",
    "prio_max_years_same_intens",
    "prio_total_episodes",
    "prio_has_interstate",
    "prio_has_internationalized",
]


def load_intermediate() -> pd.DataFrame:
    """Load the prepared conflict-level PRIO dataset from the intermediate directory."""
    if not INTERMEDIATE_PATH.exists():
        raise FileNotFoundError(
            f"Intermediate dataset not found: {INTERMEDIATE_PATH}\n"
            "Run src/data/prepare_prio_dataset.py first."
        )
    return pd.read_csv(INTERMEDIATE_PATH)


def load_base() -> pd.DataFrame:
    """Load the base conflict country-year dataset."""
    if not BASE_PATH.exists():
        raise FileNotFoundError(f"Base dataset not found: {BASE_PATH}")
    return pd.read_csv(BASE_PATH)


# ── Lifecycle helpers ────────────────────────────────────────────────────────

def _episode_duration(series: pd.Series) -> list:
    """Count consecutive years in the current uninterrupted episode per conflict."""
    result, count = [], 0
    for val in series:
        count += 1
        result.append(count)
        if val == 1:
            count = 0
    return result


def _years_same_intensity(series: pd.Series) -> list:
    """Count consecutive years at the same intensity level."""
    result, count, prev = [], 0, None
    for val in series:
        count = 1 if val != prev else count + 1
        prev = val
        result.append(count)
    return result


# ── Feature engineering ──────────────────────────────────────────────────────

def add_lifecycle_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute conflict lifecycle features grouped by conflict_id.

    Features
    --------
    conflict_age_years       : Years since the conflict first appeared in the dataset.
    n_episodes_past          : Times the conflict ended and restarted (lagged cumsum).
    is_recurring             : 1 if the conflict has had at least one past episode.
    current_episode_duration : Length of the current uninterrupted active episode.
    """
    df = df.copy()
    g = df.groupby("conflict_id")

    df["conflict_age_years"] = df["year"] - g["year"].transform("min")

    df["n_episodes_past"] = (
        g["ep_end"].transform(lambda s: s.shift(1).cumsum().fillna(0)).astype(int)
    )

    df["is_recurring"] = (df["n_episodes_past"] >= 1).astype(int)

    df["current_episode_duration"] = (
        df.groupby("conflict_id")["ep_end"].transform(_episode_duration)
    )

    return df


def add_intensity_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute intensity trajectory features grouped by conflict_id.

    Features
    --------
    intensity_lag1        : Intensity in the previous year.
    intensity_ma3         : 3-year moving average of intensity (lagged).
    intensity_trend       : Mean of last 2 years minus mean of prior 2 years.
                            Positive = escalating | zero = stable | negative = de-escalating.
    years_same_intensity  : Consecutive years at the current intensity level.
    """
    df = df.copy()
    g = df.groupby("conflict_id")

    df["intensity_lag1"] = g["intensity_level"].transform(lambda s: s.shift(1))

    df["intensity_ma3"] = g["intensity_level"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).mean()
    )

    df["intensity_trend"] = g["intensity_level"].transform(
        lambda s: (
            s.shift(1).rolling(2, min_periods=1).mean()
            - s.shift(3).rolling(2, min_periods=1).mean()
        )
    )

    df["years_same_intensity"] = (
        df.groupby("conflict_id")["intensity_level"].transform(_years_same_intensity)
    )

    return df


def collapse_to_country_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate conflict-level rows to one row per country-year.

    A country may have multiple simultaneous conflicts. Aggregation strategy:
    - Counts / sums  → total burden across all conflicts.
    - Max            → worst-case conflict in the country.
    - Mean           → average context.
    - Any-flag       → 1 if at least one conflict has that property.
    """
    df = df.copy()
    df["country"] = df["country"].str.strip().str.title()

    df_cy = (
        df.groupby(["country", "year"])
        .agg(
            prio_n_conflicts_active=(    "conflict_id",             "count"),
            prio_max_intensity=(         "intensity_level",          "max"),
            prio_max_intensity_trend=(   "intensity_trend",          "max"),
            prio_max_intensity_ma3=(     "intensity_ma3",            "max"),
            prio_mean_intensity_ma3=(    "intensity_ma3",            "mean"),
            prio_mean_conflict_age=(     "conflict_age_years",       "mean"),
            prio_any_war_level=(         "intensity_level",
                                         lambda x: int((x == 2).any())),
            prio_any_recurring=(         "is_recurring",
                                         lambda x: int((x == 1).any())),
            prio_any_cumulative_war=(    "cumulative_intensity",
                                         lambda x: int((x == 1).any())),
            prio_sum_episode_duration=(  "current_episode_duration", "sum"),
            prio_max_years_same_intens=( "years_same_intensity",     "max"),
            prio_total_episodes=(        "n_episodes_past",          "sum"),
            prio_has_interstate=(        "type_of_conflict",
                                         lambda x: int((x == 2).any())),
            prio_has_internationalized=( "type_of_conflict",
                                         lambda x: int((x == 4).any())),
        )
        .reset_index()
    )

    return df_cy


def merge_with_base(df_base: pd.DataFrame,
                    df_prio_cy: pd.DataFrame) -> pd.DataFrame:
    """
    Left-join PRIO features onto the base dataset.

    All base rows are preserved. Countries with no active conflict in PRIO
    receive 0 (absence of conflict, not missing data).
    """
    df_base    = df_base.copy()
    df_prio_cy = df_prio_cy.copy()

    df_base["country"]    = df_base["country"].str.strip().str.title()
    df_prio_cy["country"] = df_prio_cy["country"].str.strip().str.title()

    feature_cols = [c for c in df_prio_cy.columns if c.startswith("prio_")]

    df_enriched = df_base.merge(
        df_prio_cy[["country", "year"] + feature_cols],
        on=["country", "year"],
        how="left",
    )

    df_enriched[feature_cols] = df_enriched[feature_cols].fillna(0)
    return df_enriched


# ── Pipeline ─────────────────────────────────────────────────────────────────

def build_prio_features(df_intermediate: pd.DataFrame,
                        df_base: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """
    Feature engineering pipeline: lifecycle → intensity → collapse → merge.

    Expects the prepared conflict-level DataFrame from prepare_prio_dataset.py.
    Returns the enriched country-year DataFrame and the list of new feature names.
    """
    df = add_lifecycle_features(df_intermediate)
    df = add_intensity_features(df)
    df_cy = collapse_to_country_year(df)
    df_enriched = merge_with_base(df_base, df_cy)
    feature_cols = [c for c in df_enriched.columns if c.startswith("prio_")]
    return df_enriched, feature_cols


def save_dataset(df: pd.DataFrame) -> None:
    """Save the PRIO-enriched dataset to the final data directory."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")


def main() -> None:
    df_intermediate = load_intermediate()
    df_base         = load_base()

    df_enriched, feature_cols = build_prio_features(df_intermediate, df_base)
    save_dataset(df_enriched)

    print("PRIO feature dataset built successfully.")
    print(f"Input  (intermediate) : {INTERMEDIATE_PATH}")
    print(f"Input  (base)         : {BASE_PATH}")
    print(f"Output                : {OUTPUT_PATH}")
    print(f"Rows                  : {df_enriched.shape[0]}")
    print(f"Columns               : {df_enriched.shape[1]}")
    print()
    print("New PRIO features added:")
    for col in feature_cols:
        n   = (df_enriched[col] != 0).sum()
        pct = 100 * n / len(df_enriched)
        print(f"  {col:<35} {n:>8,} non-zero  ({pct:.1f}%)")


if __name__ == "__main__":
    main()
