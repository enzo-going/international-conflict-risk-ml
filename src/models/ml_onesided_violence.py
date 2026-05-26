from __future__ import annotations

from pathlib import Path
import json

import numpy as np
import pandas as pd
import geopandas as gpd

from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# =========================================================
# CONFIG
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "final"
    / "UCDP_One-sided_Violence_Dataset_updated.csv"
)

TARGET_COLUMN = "target_next_year"

TRAIN_END_YEAR = 2016


# =========================================================
# REGIONS
# =========================================================

regions = {

    "South America": [
        "Argentina",
        "Bolivia",
        "Brazil",
        "Chile",
        "Colombia",
        "Ecuador",
        "Guyana",
        "Paraguay",
        "Peru",
        "Suriname",
        "Uruguay",
        "Venezuela",
    ],

    "North America": [
        "Canada",
        "United States",
        "Mexico",
    ],

    "Central America": [
        "Guatemala",
        "Belize",
        "Honduras",
        "El Salvador",
        "Nicaragua",
        "Costa Rica",
        "Panama",
    ],

    "Caribbean": [
        "Cuba",
        "Haiti",
        "Dominican Republic",
        "Jamaica",
        "Bahamas",
    ],

    "Western Europe": [
        "France",
        "Germany",
        "Belgium",
        "Netherlands",
        "Austria",
        "Switzerland",
    ],

    "Eastern Europe": [
        "Ukraine",
        "Poland",
        "Romania",
        "Belarus",
        "Moldova",
        "Hungary",
    ],

    "Middle East": [
        "Iran",
        "Iraq",
        "Syria",
        "Israel",
        "Lebanon",
        "Jordan",
        "Saudi Arabia",
        "Yemen",
        "Turkey",
        "Palestine",
    ],

    "North Africa": [
        "Egypt",
        "Libya",
        "Tunisia",
        "Algeria",
        "Morocco",
        "Sudan",
    ],

    "West Africa": [
        "Mali",
        "Niger",
        "Nigeria",
        "Burkina Faso",
        "Ghana",
        "Senegal",
        "Guinea",
    ],

    "Central Africa": [
        "Chad",
        "Cameroon",
        "Central African Republic",
        "DR Congo",
        "Republic of Congo",
        "Gabon",
    ],

    "East Africa": [
        "Ethiopia",
        "Somalia",
        "Kenya",
        "Uganda",
        "Tanzania",
        "South Sudan",
        "Eritrea",
    ],

    "Southern Africa": [
        "South Africa",
        "Zimbabwe",
        "Mozambique",
        "Angola",
        "Botswana",
        "Namibia",
        "Zambia",
    ],

    "Central Asia": [
        "Kazakhstan",
        "Uzbekistan",
        "Turkmenistan",
        "Kyrgyzstan",
        "Tajikistan",
        "Afghanistan",
    ],

    "South Asia": [
        "India",
        "Pakistan",
        "Bangladesh",
        "Sri Lanka",
        "Nepal",
    ],

    "East Asia": [
        "China",
        "Japan",
        "North Korea",
        "South Korea",
        "Mongolia",
        "Taiwan",
    ],

    "Southeast Asia": [
        "Thailand",
        "Myanmar",
        "Vietnam",
        "Cambodia",
        "Laos",
        "Malaysia",
        "Indonesia",
        "Philippines",
    ],

    "Oceania": [
        "Australia",
        "New Zealand",
        "Papua New Guinea",
    ],
}


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("RAW DATA")
print("=" * 60)

print(df.head())
print()
print(df.columns)


# =========================================================
# CLEAN COLUMNS
# =========================================================

df.columns = (
    df.columns
    .str.lower()
    .str.strip()
)

print()
print("=" * 60)
print("CLEANED COLUMNS")
print("=" * 60)

print(df.columns.tolist())


# =========================================================
# CLEAN FATALITIES
# =========================================================

df["best_fatality_estimate"] = pd.to_numeric(
    df["best_fatality_estimate"],
    errors="coerce"
)


# =========================================================
# CLEAN LOCATION
# =========================================================

df["location"] = (
    df["location"]
    .astype(str)
    .str.split(",")
)

df = df.explode("location")

df["location"] = (
    df["location"]
    .astype(str)
    .str.strip()
)


# =========================================================
# AGGREGATE COUNTRY YEAR
# =========================================================

country_year_df = (
    df.groupby(["location", "year"])
    .agg(
        one_sided_actor_count=("actor_name", "nunique"),
        one_sided_event_count=("actor_name", "count"),

        total_fatalities=("best_fatality_estimate", "sum"),
        avg_fatalities=("best_fatality_estimate", "mean"),
        max_fatalities=("best_fatality_estimate", "max"),
    )
    .reset_index()
)


# =========================================================
# CREATE COMPLETE GRID
# =========================================================

all_years = range(
    country_year_df["year"].min(),
    country_year_df["year"].max() + 1
)

all_locations = country_year_df["location"].unique()

full_index = pd.MultiIndex.from_product(
    [all_locations, all_years],
    names=["location", "year"]
)

full_df = pd.DataFrame(index=full_index).reset_index()


# =========================================================
# MERGE
# =========================================================

country_year_df = full_df.merge(
    country_year_df,
    on=["location", "year"],
    how="left"
)


# =========================================================
# FILL MISSING VALUES
# =========================================================

fill_columns = [
    "one_sided_actor_count",
    "one_sided_event_count",
    "total_fatalities",
    "avg_fatalities",
    "max_fatalities",
]

for col in fill_columns:
    country_year_df[col] = (
        country_year_df[col]
        .fillna(0)
    )


# =========================================================
# CREATE VIOLENCE FLAG
# =========================================================

country_year_df["one_sided_violence_exists"] = np.where(
    country_year_df["one_sided_event_count"] > 0,
    1,
    0,
)


# =========================================================
# SORT
# =========================================================

country_year_df = country_year_df.sort_values(
    ["location", "year"]
)

print()
print("=" * 60)
print("COUNTRY YEAR DATASET")
print("=" * 60)

print(country_year_df.head())


# =========================================================
# TEMPORAL FEATURES
# =========================================================

country_year_df["previous_year_violence"] = (
    country_year_df
    .groupby("location")["one_sided_violence_exists"]
    .shift(1)
)

country_year_df["violence_last_3_years"] = (
    country_year_df
    .groupby("location")["one_sided_violence_exists"]
    .transform(
        lambda x: (
            x.shift(1)
            .rolling(3, min_periods=1)
            .sum()
        )
    )
)

country_year_df["violence_last_5_years"] = (
    country_year_df
    .groupby("location")["one_sided_violence_exists"]
    .transform(
        lambda x: (
            x.shift(1)
            .rolling(5, min_periods=1)
            .sum()
        )
    )
)

country_year_df["cumulative_events"] = (
    country_year_df
    .groupby("location")["one_sided_event_count"]
    .cumsum()
)

country_year_df["fatalities_last_3_years"] = (
    country_year_df
    .groupby("location")["total_fatalities"]
    .transform(
        lambda x: (
            x.shift(1)
            .rolling(3, min_periods=1)
            .sum()
        )
    )
)

country_year_df["fatalities_last_5_years"] = (
    country_year_df
    .groupby("location")["total_fatalities"]
    .transform(
        lambda x: (
            x.shift(1)
            .rolling(5, min_periods=1)
            .sum()
        )
    )
)

country_year_df["previous_year_fatalities"] = (
    country_year_df
    .groupby("location")["total_fatalities"]
    .shift(1)
)


# =========================================================
# YEARS SINCE LAST VIOLENCE
# =========================================================

country_year_df["years_since_last_violence"] = (
    country_year_df
    .groupby("location")["one_sided_violence_exists"]
    .transform(
        lambda x: (
            x.groupby(
                x.eq(1).cumsum()
            ).cumcount()
        )
    )
)


# =========================================================
# FATALITY GROWTH RATE
# =========================================================

country_year_df["fatality_growth_rate"] = (
    country_year_df["total_fatalities"]
    /
    (
        country_year_df["previous_year_fatalities"]
        + 1
    )
)


# =========================================================
# REGIONS
# =========================================================

location_to_region = {}

for region, countries in regions.items():
    for country in countries:
        location_to_region[country] = region

country_year_df["region"] = (
    country_year_df["location"]
    .map(location_to_region)
)


# =========================================================
# BUILD GLOBAL NEIGHBOR TABLE
# =========================================================

print()
print("=" * 60)
print("BUILDING GLOBAL NEIGHBOR TABLE")
print("=" * 60)

world = gpd.read_file(
    "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
)
# =========================================================
# FIX COUNTRY NAMES
# =========================================================

country_name_fixes = {

    # GeoPandas / Natural Earth
    "United States of America": "United States",
    "Dem. Rep. Congo": "DR Congo",
    "Central African Rep.": "Central African Republic",
    "Bosnia and Herz.": "Bosnia-Herzegovina",

    # Dataset aliases
    "Ivory Coast": "Côte d'Ivoire",
    "Myanmar (Burma)": "Myanmar",
    "Cambodia (Kampuchea)": "Cambodia",
    "Russia (Soviet Union)": "Russia",
    "Zimbabwe (Rhodesia)": "Zimbabwe",
    "Kingdom of eSwatini (Swaziland)": "eSwatini",
    "DR Congo (Zaire)": "DR Congo",
    "Serbia (Yugoslavia)": "Serbia",
    "Yemen (North Yemen)": "Yemen",

    # Extra fixes
    "South Sudan": "S. Sudan",
    "Bahrain": "Bahrain",
}

# =========================================================
# FIX WORLD COUNTRY NAMES
# =========================================================

world["NAME"] = (
    world["NAME"]
    .replace(country_name_fixes)
)

# =========================================================
# FIX DATASET COUNTRY NAMES
# =========================================================

country_year_df["location"] = (
    country_year_df["location"]
    .replace(country_name_fixes)
)

# =========================================================
# CREATE NEIGHBOR TABLE
# =========================================================

neighbors = {}

for idx, country in world.iterrows():

    country_name = country["NAME"]

    touching = world[
        world.geometry.touches(country.geometry)
    ]

    neighbors[country_name] = (
        touching["NAME"].tolist()
    )
    

print(f"Countries with neighbors: {len(neighbors)}")


# =========================================================
# FIND MISSING COUNTRIES
# =========================================================

missing = country_year_df[
    ~country_year_df["location"].isin(neighbors.keys())
]["location"].unique()

print()
print("=" * 60)
print("COUNTRIES NOT MATCHED")
print("=" * 60)

print(missing)


# =========================================================
# NEIGHBORING CONFLICT
# =========================================================

country_year_df["neighboring_conflict"] = 0

for idx, row in country_year_df.iterrows():

    country = row["location"]
    year = row["year"]

    if country not in neighbors or len(neighbors[country]) == 0:
        continue

    neighbor_list = neighbors[country]

    neighbor_conflicts = country_year_df[
        (
            country_year_df["location"]
            .isin(neighbor_list)
        )
        &
        (
            country_year_df["year"] == year
        )
    ]["one_sided_violence_exists"].sum()

    country_year_df.at[
        idx,
        "neighboring_conflict"
    ] = neighbor_conflicts


# =========================================================
# CREATE TARGET
# =========================================================

country_year_df[TARGET_COLUMN] = (
    country_year_df
    .groupby("location")["one_sided_violence_exists"]
    .shift(-1)
)

country_year_df[TARGET_COLUMN] = (
    country_year_df[TARGET_COLUMN]
    .fillna(0)
    .astype(int)
)

print()
print("=" * 60)
print("TARGET DISTRIBUTION")
print("=" * 60)

print(
    country_year_df[TARGET_COLUMN]
    .value_counts()
)


# =========================================================
# FILL NULLS
# =========================================================

country_year_df = country_year_df.fillna(0)


# =========================================================
# FEATURES
# =========================================================

FEATURE_COLUMNS = [

    "one_sided_actor_count",

    "previous_year_violence",
    "violence_last_3_years",
    "violence_last_5_years",

    "cumulative_events",

    "total_fatalities",
    "avg_fatalities",
    "max_fatalities",

    "fatalities_last_3_years",
    "fatalities_last_5_years",

    "previous_year_fatalities",

    "years_since_last_violence",
    "fatality_growth_rate",

    "neighboring_conflict",
]

print()
print("=" * 60)
print("FEATURES")
print("=" * 60)

for feature in FEATURE_COLUMNS:
    print(feature)


# =========================================================
# TRAIN TEST SPLIT
# =========================================================

train_mask = (
    country_year_df["year"]
    <= TRAIN_END_YEAR
)

test_mask = (
    country_year_df["year"]
    > TRAIN_END_YEAR
)

X_train = country_year_df.loc[
    train_mask,
    FEATURE_COLUMNS,
]

y_train = country_year_df.loc[
    train_mask,
    TARGET_COLUMN,
]

X_test = country_year_df.loc[
    test_mask,
    FEATURE_COLUMNS,
]

y_test = country_year_df.loc[
    test_mask,
    TARGET_COLUMN,
]

print()
print("=" * 60)
print("TRAIN TEST SPLIT")
print("=" * 60)

print(f"Train rows: {len(X_train)}")
print(f"Test rows: {len(X_test)}")


# =========================================================
# MODEL
# =========================================================

model = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),
        (
            "scaler",
            StandardScaler(),
        ),
        (
            "model",
            LogisticRegression(
                max_iter=5000,
                class_weight="balanced",
                random_state=42,
            ),
        ),
    ]
)


# =========================================================
# TRAIN
# =========================================================

model.fit(X_train, y_train)


# =========================================================
# PREDICT
# =========================================================

y_pred = model.predict(X_test)

y_proba = model.predict_proba(X_test)[:, 1]


# =========================================================
# METRICS
# =========================================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0,
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0,
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0,
)

roc_auc = roc_auc_score(
    y_test,
    y_proba,
)

tn, fp, fn, tp = confusion_matrix(
    y_test,
    y_pred,
).ravel()


# =========================================================
# FEATURE IMPORTANCE
# =========================================================

coefficients = (
    model.named_steps["model"]
    .coef_[0]
)

importance_df = pd.DataFrame({
    "feature": FEATURE_COLUMNS,
    "coefficient": coefficients,
    "absolute_value": np.abs(coefficients),
})

importance_df = importance_df.sort_values(
    "absolute_value",
    ascending=False,
)


# =========================================================
# RESULTS
# =========================================================

print()
print("=" * 60)
print("MODEL RESULTS")
print("=" * 60)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC AUC  : {roc_auc:.4f}")

print()
print("=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

print(f"TN: {tn}")
print(f"FP: {fp}")
print(f"FN: {fn}")
print(f"TP: {tp}")


# =========================================================
# FEATURE IMPORTANCE
# =========================================================

print()
print("=" * 60)
print("FEATURE IMPORTANCE")
print("=" * 60)

print(
    importance_df
    .round(4)
    .to_string(index=False)
)


# =========================================================
# PREDICTIONS
# =========================================================

results_df = country_year_df.loc[
    test_mask,
    [
        "location",
        "year",
        TARGET_COLUMN,
    ],
].copy()

results_df["predicted"] = y_pred

results_df["probability"] = y_proba


print()
print("=" * 60)
print("PREDICTIONS SAMPLE")
print("=" * 60)

print(
    results_df
    .head(20)
    .round(4)
    .to_string(index=False)
)


# =========================================================
# SAVE OUTPUTS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"

OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)

results_df.to_csv(
    OUTPUT_TABLES_DIR / "one_sided_predictions.csv",
    index=False,
)

importance_df.to_csv(
    OUTPUT_TABLES_DIR / "one_sided_feature_importance.csv",
    index=False,
)

with open(
    OUTPUT_TABLES_DIR / "neighbors.json",
    "w"
) as f:
    json.dump(neighbors, f, indent=4)


print()
print("=" * 60)
print("FILES SAVED")
print("=" * 60)

print("one_sided_predictions.csv")
print("one_sided_feature_importance.csv")
print("neighbors.json")