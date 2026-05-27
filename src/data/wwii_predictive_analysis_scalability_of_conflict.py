from pathlib import Path

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

# ============================================================
# RANDOM SEED
# ============================================================

GLOBAL_RANDOM_STATE = 42
np.random.seed(GLOBAL_RANDOM_STATE)

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ============================================================
# DATA PATH
# ============================================================

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

    print("\nLoading WWII Dataset...")

    df = pd.read_csv(
        WW2_DATA
    )

    df["war_name"] = "WWII"

    df["event_id"] = (
        "WWII_" +
        df["event_id"].astype(str)
    )

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    return df