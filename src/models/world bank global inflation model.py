from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

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
    / "inflation_country_year_clean.csv"
)

TARGET_COLUMN = "high_inflation_next_year"

TRAIN_END_YEAR = 2016

HIGH_INFLATION_THRESHOLD = 10


# =========================================================
# LOAD DATA
# =========================================================

print("=" * 60)
print("LOADING DATASET")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

print(df.head())
print()
print(df.columns)


# =========================================================
# SORT
# =========================================================

df = df.sort_values([
    "country",
    "year",
])


# =========================================================
# CREATE TARGET
# =========================================================

df["next_year_inflation"] = (
    df
    .groupby("country")
    ["inflation_consumer_prices_annual_pct"]
    .shift(-1)
)

df[TARGET_COLUMN] = np.where(
    df["next_year_inflation"] >= HIGH_INFLATION_THRESHOLD,
    1,
    0,
)


# =========================================================
# TEMPORAL FEATURES
# =========================================================

df["inflation_previous_year"] = (
    df
    .groupby("country")
    ["inflation_consumer_prices_annual_pct"]
    .shift(1)
)

df["inflation_last_3_years_mean"] = (
    df
    .groupby("country")
    ["inflation_consumer_prices_annual_pct"]
    .transform(
        lambda x: (
            x.shift(1)
            .rolling(3, min_periods=1)
            .mean()
        )
    )
)

df["inflation_last_5_years_mean"] = (
    df
    .groupby("country")
    ["inflation_consumer_prices_annual_pct"]
    .transform(
        lambda x: (
            x.shift(1)
            .rolling(5, min_periods=1)
            .mean()
        )
    )
)

df["inflation_growth_rate"] = (
    df["inflation_consumer_prices_annual_pct"]
    /
    (
        df["inflation_previous_year"] + 1
    )
)

df["inflation_volatility_5y"] = (
    df
    .groupby("country")
    ["inflation_consumer_prices_annual_pct"]
    .transform(
        lambda x: (
            x.shift(1)
            .rolling(5, min_periods=1)
            .std()
        )
    )
)


# =========================================================
# CLEAN NULLS
# =========================================================

df = df.fillna(0)


# =========================================================
# FEATURES
# =========================================================

FEATURE_COLUMNS = [
    "inflation_consumer_prices_annual_pct",
    "inflation_previous_year",
    "inflation_last_3_years_mean",
    "inflation_last_5_years_mean",
    "inflation_growth_rate",
    "inflation_volatility_5y",
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
    df["year"] <= TRAIN_END_YEAR
)

test_mask = (
    df["year"] > TRAIN_END_YEAR
)

X_train = df.loc[
    train_mask,
    FEATURE_COLUMNS,
]

y_train = df.loc[
    train_mask,
    TARGET_COLUMN,
]

X_test = df.loc[
    test_mask,
    FEATURE_COLUMNS,
]

y_test = df.loc[
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

results_df = df.loc[
    test_mask,
    [
        "country",
        "year",
        "inflation_consumer_prices_annual_pct",
        TARGET_COLUMN,
    ],
].copy()

results_df["predicted_high_inflation"] = y_pred

results_df["predicted_probability"] = y_proba


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

OUTPUT_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "tables"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

results_df.to_csv(
    OUTPUT_DIR / "inflation_predictions.csv",
    index=False,
)

importance_df.to_csv(
    OUTPUT_DIR / "inflation_feature_importance.csv",
    index=False,
)

print()
print("=" * 60)
print("FILES SAVED")
print("=" * 60)

print("inflation_predictions.csv")
print("inflation_feature_importance.csv")