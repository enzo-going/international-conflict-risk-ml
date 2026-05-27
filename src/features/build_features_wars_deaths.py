import numpy as np

from sklearn.preprocessing import LabelEncoder

TARGET_COLUMN = "next_month_escalation"

# ============================================================
# FEATURE ENGINEERING
# ============================================================

def build_features(df):

    print("\nBuilding Features...")

    categorical_cols = [
        "country",
        "alliance",
        "front",
        "war_name"
    ]

    for col in categorical_cols:

        encoder = LabelEncoder()

        df[col + "_encoded"] = (
            encoder.fit_transform(df[col])
        )

    df = df.sort_values(
        ["conflict_id", "time_index"]
    ).reset_index(drop=True)

    grouped = df.groupby(
        "conflict_id"
    )

    for lag in [1, 2, 3]:

        df[f"lag_{lag}"] = (

            grouped["current_deaths"]
            .shift(lag)
        )

    df["delta_1"] = (

        df["current_deaths"] -

        df["lag_1"]
    )

    df["delta_2"] = (

        df["lag_1"] -

        df["lag_2"]
    )

    df["growth_rate"] = (

        np.log1p(
            df["current_deaths"]
        ) -

        np.log1p(
            df["lag_1"]
        )
    )

    rolling_3 = grouped[
        "current_deaths"
    ].rolling(
        3,
        min_periods=1
    )

    rolling_6 = grouped[
        "current_deaths"
    ].rolling(
        6,
        min_periods=1
    )

    df["rolling_mean_3"] = (

        rolling_3.mean()

        .reset_index(
            level=0,
            drop=True
        )
    )

    df["rolling_mean_6"] = (

        rolling_6.mean()

        .reset_index(
            level=0,
            drop=True
        )
    )

    df["rolling_std_6"] = (

        rolling_6.std()

        .reset_index(
            level=0,
            drop=True
        )
    )

    df["ewma_6"] = (

        grouped["current_deaths"]

        .transform(
            lambda x:
            x.ewm(span=6).mean()
        )
    )

    df["momentum"] = (

        df["current_deaths"] -

        df["rolling_mean_3"]
    )

    df["volatility"] = (

        df["rolling_std_6"] /

        (
            df["rolling_mean_6"] + 1e-6
        )
    )

    df["acceleration"] = (

        grouped["delta_1"]
        .diff()
    )

    df["next_month_deaths"] = (

        grouped["current_deaths"]
        .shift(-1)
    )

    escalation_ratio = (

        df["next_month_deaths"] /

        (
            df["current_deaths"] + 1e-6
        )
    )

    df[TARGET_COLUMN] = (

        escalation_ratio > 1.50

    ).astype(int)

    df = df.dropna(
        subset=["next_month_deaths"]
    ).copy()

    features = [

        "current_deaths",

        "lag_1",
        "lag_2",
        "lag_3",

        "delta_1",
        "delta_2",

        "growth_rate",

        "rolling_mean_3",
        "rolling_mean_6",

        "rolling_std_6",

        "ewma_6",

        "momentum",
        "volatility",
        "acceleration",

        "casualties_mil_k",
        "casualties_civ_k",
        "military_personnel_k",
        "casualty_ratio",

        "country_encoded",
        "alliance_encoded",
        "front_encoded",
        "war_name_encoded"
    ]

    df[features] = (

        df[features]

        .replace(
            [np.inf, -np.inf],
            0
        )

        .fillna(0)
    )

    print("\nFeature Engineering Completed.")

    print("\nTarget Distribution:")

    print(
        df[TARGET_COLUMN]
        .value_counts(normalize=True)
    )

    return df, features