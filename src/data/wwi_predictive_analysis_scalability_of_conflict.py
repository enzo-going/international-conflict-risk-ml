from pathlib import Path

import pandas as pd

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ============================================================
# DATA PATHS
# ============================================================

DATA_DIR = PROJECT_ROOT / "data" / "final"

WW1_DATA = (
    DATA_DIR /
    "world_war_1_details_clean.csv"
)

# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("\nLoading WWI Dataset...")

    df = pd.read_csv(WW1_DATA)

    df["war_name"] = "WWI"

    df["event_id"] = (
        "WWI_" +
        df["event_id"].astype(str)
    )

    print("\nDataset Shape:")
    print(df.shape)

    return df