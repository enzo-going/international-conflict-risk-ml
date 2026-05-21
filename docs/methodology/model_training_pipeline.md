# Model Training Pipeline

This document describes the current main training pipeline of the project.

## Current goal

The current objective is to train a supervised classification model to estimate whether a country will present organized violence in the following year.

The prediction target is:

`target_conflict_next_year`

This is not a deterministic prediction of global war. It is a country-year classification task based on historical conflict patterns and external socioeconomic indicators.

## Input dataset

The current main dataset is:

`data/final/conflict_country_year_world_bank_features.csv`

This dataset combines:

- UCDP Organized Violence country-year data;
- temporal conflict features;
- World Bank socioeconomic indicators;
- engineered World Bank temporal features.

## Unit of analysis

The unit of analysis is:

`country-year`

Each row represents one country in one year.

## Train/test strategy

The project uses a temporal split:

- training period: 1989 to 2016;
- test period: 2017 to 2023.

This avoids random mixing of past and future observations and provides a more realistic evaluation.

## Baseline

The main baseline is the persistence baseline:

`y_pred = organized_violence_exists`

This means that if a country had organized violence in the current year, the baseline predicts organized violence in the following year.

This baseline is intentionally simple, but strong, because conflict has high temporal persistence.

## Current main model

The current main model is a scikit-learn pipeline:

1. `SimpleImputer(strategy="median")`
2. `StandardScaler()`
3. `LogisticRegression(class_weight="balanced", max_iter=5000, random_state=42)`

The training script is:

`src/models/train_conflict_risk_model.py`

## Feature groups

The model uses the following feature groups:

1. UCDP conflict variables;
2. temporal conflict features;
3. raw World Bank indicators;
4. engineered World Bank features.

Engineered World Bank features include:

- lagged values;
- annual changes;
- rolling 3-year means;
- missing-value flags.

## Output artifacts

The training script generates:

| Artifact | Path |
|---|---|
| trained model | `outputs/models/conflict_risk_logistic_regression_pipeline.joblib` |
| feature metadata | `outputs/models/conflict_risk_model_features.json` |
| model metrics | `outputs/tables/conflict_risk_model_metrics.csv` |
| test predictions | `outputs/tables/conflict_risk_model_test_predictions.csv` |

## Current result

| Model | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|
| Persistence baseline | 0.9072 | 0.8571 | 0.8571 | 0.8571 |
| Logistic Regression + engineered World Bank features | 0.9175 | 0.8926 | 0.8481 | 0.8698 |

The current main model improves F1-score over the persistence baseline by approximately:

`+0.0126`

## Interpretation

The result suggests that adding heterogeneous socioeconomic data from the World Bank only becomes useful after feature engineering.

Raw World Bank indicators alone did not improve the best model, but lagged values, annual changes, rolling means and missing-value flags produced the best result observed so far.

The improvement is moderate, but methodologically relevant.

## Current limitations

- The model is still a classical ML baseline, not yet a neural network.
- The predicted probabilities are not calibrated yet.
- The threshold is still the default 0.5.
- Only one external dataset family, World Bank, has been integrated so far.
- Some historical countries/entities were excluded from the World Bank merge due to mapping limitations.

## Next technical steps

Recommended next steps:

1. evaluate probability calibration;
2. test threshold tuning;
3. test stronger tabular models, such as gradient boosting;
4. test a small neural network as a comparative model;
5. update the dashboard with the current main algorithm result.
