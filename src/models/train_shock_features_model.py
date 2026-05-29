import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

DATA_PATH = "data/final/conflict_country_year_world_bank_features.csv"
OUTPUT_PATH = "outputs/tables/shock_features_experiment_results.csv"
TRAIN_END_YEAR = 2016
TEST_START_YEAR = 2017
TARGET = "target_conflict_next_year"
BASELINE_F1 = 0.857143
CURRENT_MODEL_F1 = 0.872216

FEATURES_BASE = [
    "year",
    "state_based_conflict_exists", "state_based_dyad_count", "state_based_deaths_best",
    "intrastate_conflict_exists", "intrastate_deaths_best",
    "interstate_conflict_exists", "interstate_deaths_best",
    "non_state_conflict_exists", "non_state_dyad_count", "non_state_deaths_best",
    "one_sided_violence_exists", "one_sided_dyad_count", "one_sided_deaths_best",
    "cumulative_organized_violence_deaths_best", "organized_violence_exists",
    "conflict_previous_year", "conflict_last_3_years_count", "conflict_last_5_years_count",
    "deaths_previous_year", "deaths_last_3_years_sum", "deaths_last_5_years_sum",
    "years_since_last_conflict",
    "population_total", "population_growth_annual_pct", "urban_population_pct",
    "gdp_per_capita_current_usd", "gdp_growth_annual_pct",
    "inflation_consumer_prices_annual_pct", "unemployment_total_pct",
    "school_enrollment_secondary_gross_pct",
    "military_expenditure_pct_gdp", "natural_resources_rents_pct_gdp",
]

FEATURES_SHOCK = [
    "gdp_growth_annual_pct_change_1y",
    "gdp_per_capita_current_usd_change_1y",
    "inflation_consumer_prices_annual_pct_change_1y",
    "military_expenditure_pct_gdp_change_1y",
    "gdp_growth_annual_pct_rolling_3y_mean",
    "gdp_per_capita_current_usd_lag1",
]

def evaluate(y_true, y_pred, label, n_features):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    f1 = f1_score(y_true, y_pred)
    return {
        "experiment": label,
        "n_features": n_features,
        "accuracy": round(accuracy_score(y_true, y_pred), 6),
        "precision": round(precision_score(y_true, y_pred), 6),
        "recall": round(recall_score(y_true, y_pred), 6),
        "f1_score": round(f1, 6),
        "tn": tn, "fp": fp, "fn": fn, "tp": tp,
        "f1_vs_official_baseline": round(f1 - BASELINE_F1, 6),
        "f1_vs_official_current_model": round(f1 - CURRENT_MODEL_F1, 6),
    }

def train_and_eval(df_train, df_test, features, label):
    X_train = df_train[features]
    y_train = df_train[TARGET]
    X_test = df_test[features]
    y_test = df_test[TARGET]
    pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)),
    ])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    return evaluate(y_test, y_pred, label, len(features))

def main():
    df = pd.read_csv(DATA_PATH)
    print("Dataset carregado:", df.shape)

    missing = [f for f in FEATURES_SHOCK if f not in df.columns]
    if missing:
        print("AVISO - features ausentes:", missing)
    features_shock_available = [f for f in FEATURES_SHOCK if f in df.columns]
    print("Features de choque disponiveis:", len(features_shock_available))

    df_train = df[df["year"] <= TRAIN_END_YEAR].copy()
    df_test = df[df["year"] >= TEST_START_YEAR].copy()
    print("Treino:", len(df_train), "| Teste:", len(df_test))

    results = []

    y_test_all = df_test[TARGET]
    y_baseline = df_test["conflict_previous_year"].astype(int)
    results.append(evaluate(y_test_all, y_baseline, "persistence_baseline", 1))
    results.append(train_and_eval(df_train, df_test, FEATURES_BASE, "base_model_replicated"))

    features_extended = FEATURES_BASE + features_shock_available
    results.append(train_and_eval(df_train, df_test, features_extended, "base_plus_shock_features"))

    features_minimal = ["conflict_previous_year", "years_since_last_conflict"] + features_shock_available
    results.append(train_and_eval(df_train, df_test, features_minimal, "shock_only_control"))

    df_results = pd.DataFrame(results)
    df_results.to_csv(OUTPUT_PATH, index=False)

    print("\n=== RESULTADOS ===")
    print(df_results[["experiment", "n_features", "f1_score", "f1_vs_official_baseline", "f1_vs_official_current_model"]].to_string(index=False))
    print("\nSalvo em:", OUTPUT_PATH)

if __name__ == "__main__":
    main()
