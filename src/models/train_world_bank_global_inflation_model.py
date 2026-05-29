from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from xgboost import XGBClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)



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

GDP_PATH = (
    PROJECT_ROOT
    / "data"
    / "final"
    / "gdp_per_capita_usd.csv"
)

GDP_GROWTH_PATH = (
    PROJECT_ROOT
    / "data"
    / "final"
    / "gdp_growth_ml_ready.csv"
)

INTEREST_RATE_PATH = (
    PROJECT_ROOT
    / "data"
    / "final"
    / "real_interest_rate_ml_ready.csv"
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
gdp_df = pd.read_csv(GDP_PATH)
gdp_growth_df = pd.read_csv(GDP_GROWTH_PATH)
interest_df = pd.read_csv(INTEREST_RATE_PATH)

df = df.merge(
    gdp_df,
    on=["country", "year"],
    how="left",
)

df = df.merge(
    gdp_growth_df,
    on=["country", "year"],
    how="left",
)

df = df.merge(
    interest_df,
    on=["country", "year"],
    how="left",
)

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

df["gdp_previous_year"] = (
    df.groupby("country")["gdp_per_capita_current_usd"]
    .shift(1)
)

df["gdp_growth_rate"] = (
    df["gdp_per_capita_current_usd"]
    /
    (df["gdp_previous_year"] + 1)
)

df["gdp_last_3_years_mean"] = (
    df.groupby("country")["gdp_per_capita_current_usd"]
    .transform(
        lambda x: (
            x.shift(1)
            .rolling(3, min_periods=1)
            .mean()
        )
    )
)

df["gdp_growth_previous_year"] = (
    df.groupby("country")["gdp_growth"]
    .shift(1)
)

df["gdp_growth_last_3_years_mean"] = (
    df.groupby("country")["gdp_growth"]
    .transform(
        lambda x: (
            x.shift(1)
            .rolling(3, min_periods=1)
            .mean()
        )
    )
)

df["gdp_growth_volatility"] = (
    df.groupby("country")["gdp_growth"]
    .transform(
        lambda x: (
            x.shift(1)
            .rolling(3, min_periods=1)
            .std()
        )
    )
)

df["interest_previous_year"] = (
    df.groupby("country")["real_interest_rate"]
    .shift(1)
)

df["interest_last_3_years_mean"] = (
    df.groupby("country")["real_interest_rate"]
    .transform(
        lambda x: (
            x.shift(1)
            .rolling(3, min_periods=1)
            .mean()
        )
    )
)

df["interest_volatility"] = (
    df.groupby("country")["real_interest_rate"]
    .transform(
        lambda x: (
            x.shift(1)
            .rolling(3, min_periods=1)
            .std()
        )
    )
)

df["inflation_interest_interaction"] = (
    df["inflation_previous_year"]
    *
    df["real_interest_rate"]
)

df["gdp_interest_interaction"] = (
    df["gdp_growth"]
    *
    df["real_interest_rate"]
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
    
    "gdp_per_capita_current_usd",
    "gdp_previous_year",
    "gdp_growth_rate",
    "gdp_last_3_years_mean",
    
    "gdp_growth_previous_year",
    "gdp_growth_last_3_years_mean",
    "gdp_growth_volatility",
    
    "real_interest_rate",
    "interest_previous_year",
    "interest_last_3_years_mean",
    "interest_volatility",
    
    "inflation_interest_interaction",
    "gdp_interest_interaction",
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
# MODEL - XGBOOST
# =========================================================

model = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),

        (
            "model",
            XGBClassifier(

                # trees
                n_estimators=300,
                max_depth=6,

                # learning
                learning_rate=0.05,

                # randomness
                subsample=0.8,
                colsample_bytree=0.8,

                # imbalance handling
                scale_pos_weight=2,

                # regularization
                reg_alpha=0.5,
                reg_lambda=1,

                # performance
                random_state=42,
                eval_metric="logloss",
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

importances = (
    model.named_steps["model"]
    .feature_importances_
)

importance_df = pd.DataFrame({
    "feature": FEATURE_COLUMNS,
    "importance": importances,
})

importance_df = importance_df.sort_values(
    "importance",
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