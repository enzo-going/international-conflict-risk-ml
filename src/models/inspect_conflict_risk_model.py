from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "outputs" / "models" / "conflict_risk_logistic_regression_pipeline.joblib"
FEATURES_PATH = PROJECT_ROOT / "outputs" / "models" / "conflict_risk_model_features.json"

OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
OUTPUT_PATH = OUTPUT_TABLES_DIR / "conflict_risk_model_coefficients.csv"


def classify_effect(coefficient: float) -> str:
    if coefficient > 0:
        return "increases_predicted_risk"
    if coefficient < 0:
        return "decreases_predicted_risk"
    return "neutral"


def classify_feature_group(feature: str) -> str:
    world_bank_terms = [
        "population",
        "gdp",
        "inflation",
        "unemployment",
        "military",
        "school",
        "urban",
        "natural_resources",
    ]

    temporal_terms = [
        "previous_year",
        "last_3_years",
        "last_5_years",
        "years_since",
    ]

    conflict_terms = [
        "conflict",
        "violence",
        "deaths",
        "dyad",
        "intrastate",
        "interstate",
        "non_state",
        "one_sided",
    ]

    if any(term in feature for term in world_bank_terms):
        return "world_bank"

    if any(term in feature for term in temporal_terms):
        return "temporal_conflict"

    if any(term in feature for term in conflict_terms):
        return "ucdp_conflict"

    if feature == "year":
        return "time_index"

    return "other"


def main() -> None:
    OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)

    model_pipeline = joblib.load(MODEL_PATH)

    metadata = json.loads(FEATURES_PATH.read_text(encoding="utf-8"))
    feature_columns = metadata["feature_columns"]

    logistic_model = model_pipeline.named_steps["model"]
    coefficients = logistic_model.coef_[0]

    if len(feature_columns) != len(coefficients):
        raise ValueError(
            "Feature count mismatch: "
            f"{len(feature_columns)} feature names vs {len(coefficients)} coefficients."
        )

    coefficients_df = pd.DataFrame(
        {
            "feature": feature_columns,
            "coefficient": coefficients,
        }
    )

    coefficients_df["absolute_coefficient"] = coefficients_df["coefficient"].abs()
    coefficients_df["effect"] = coefficients_df["coefficient"].apply(classify_effect)
    coefficients_df["feature_group"] = coefficients_df["feature"].apply(classify_feature_group)

    coefficients_df = coefficients_df.sort_values(
        by="absolute_coefficient",
        ascending=False,
    ).reset_index(drop=True)

    coefficients_df["rank"] = coefficients_df.index + 1

    coefficients_df = coefficients_df[
        [
            "rank",
            "feature",
            "feature_group",
            "coefficient",
            "absolute_coefficient",
            "effect",
        ]
    ]

    coefficients_df.to_csv(OUTPUT_PATH, index=False)

    print("Conflict risk model coefficient inspection completed.")
    print(f"Model: {MODEL_PATH}")
    print(f"Feature metadata: {FEATURES_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print()
    print(f"Features analyzed: {len(coefficients_df)}")
    print()
    print("Top 15 features by absolute coefficient:")
    print(coefficients_df.head(15).to_string(index=False))

    print()
    print("Feature group counts:")
    print(coefficients_df["feature_group"].value_counts().to_string())


if __name__ == "__main__":
    main()