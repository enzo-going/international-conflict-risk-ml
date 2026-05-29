from pathlib import Path

import pandas as pd

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ============================================================
# DATA PATHS
# ============================================================

WW1_DATA = (
    PROJECT_ROOT /
    "data" /
    "final" /
    "world_war_1_details_clean.csv"
)

WW2_DATA = (
    PROJECT_ROOT /
    "data" /
    "final" /
    "world_war_2_clean.csv"
)

# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("\nLoading WWI + WWII Dataset...")

    ww1 = pd.read_csv(
        WW1_DATA
    )

    ww2 = pd.read_csv(
        WW2_DATA
    )

    ww1["war_name"] = "WWI"
    ww2["war_name"] = "WWII"

    ww1["event_id"] = (
        "WWI_" +
        ww1["event_id"].astype(str)
    )

    ww2["event_id"] = (
        "WWII_" +
        ww2["event_id"].astype(str)
    )

    ww1["war_type"] = 0
    ww2["war_type"] = 1

    df = pd.concat(
        [ww1, ww2],
        ignore_index=True
    )

    print("\nDataset Shape:")
    print(df.shape)

    print("\nWars:")
    print(
        df["war_name"]
        .value_counts()
    )

    return df