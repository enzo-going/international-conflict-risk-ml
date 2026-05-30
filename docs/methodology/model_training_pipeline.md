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
- raw World Bank socioeconomic indicators.

Therefore, the official pipeline state is:

`UCDP Organized Violence + temporal conflict features + World Bank indicators`

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

The current official feature set contains 33 features:

- 16 UCDP conflict/base variables;
- 7 temporal conflict features;
- 10 raw World Bank indicators.

The training script is:

`src/models/train_conflict_risk_model.py`

## Feature groups

The model uses the following feature groups:

1. UCDP conflict variables;
2. temporal conflict features;
3. raw World Bank indicators.

The current main model uses the raw World Bank indicators, not the engineered World Bank lag/change/rolling features. Engineered World Bank features are still generated and evaluated in experiments, but are not part of the current main model because the ablation analysis showed better performance without them.

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
| Logistic Regression + World Bank all raw | 0.9197 | 0.9029 | 0.8435 | 0.8722 |

The current main model improves F1-score over the persistence baseline by approximately:

`+0.0151`

## Interpretation

The ablation analysis showed that the best current model uses the complete raw World Bank indicator set without the engineered World Bank temporal features.

The improvement over the persistence baseline is small/moderate, but methodologically relevant. It should be interpreted with caution: most predictive signal still comes from historical conflict persistence, and the model should not be presented as a deterministic forecasting system or as a model for predicting a world war.

## Current limitations

- The model is still a classical ML model.
- Probability/threshold analyses exist as diagnostics, but the official model still uses the default binary decision rule in the main training script.
- Only one external dataset family, World Bank, has been integrated so far.
- Some historical countries/entities were excluded from the World Bank merge due to mapping limitations.
- SIPRI, PRIO, WWI/WWII, One-Sided Violence, shock features and global inflation analyses are experimental or supporting modules unless explicitly integrated into the official `country-year` pipeline.

## Next technical steps

Recommended next steps:

1. consolidate documentation around the current 33-feature official model;
2. validate feature selection and stability before adding new external datasets;
3. keep experimental modules separated from the official UCDP + World Bank pipeline;
4. evaluate probability calibration more formally before using risk bands as operational claims;
5. treat new sources such as SIPRI or PRIO as candidates requiring key, coverage, missingness and row-loss validation before integration.
