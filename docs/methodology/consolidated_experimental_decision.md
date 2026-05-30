# Consolidated Experimental Decision

## Current official model

The current official model is:

- Model: Logistic Regression scaled - World Bank all raw
- Feature count: 33
- Accuracy: 0.9197
- Precision: 0.9029
- Recall: 0.8435
- F1-score: 0.8722
- Persistence baseline F1-score: 0.8571
- F1 gain over persistence: +0.0151

## Main interpretation

The official model provides a moderate but real improvement over the persistence baseline. This is methodologically relevant because persistence is a strong benchmark in conflict prediction: countries with recent organized violence tend to remain at higher risk.

However, the gain is small. Therefore, the result should be presented as an incremental predictive improvement, not as a strong operational forecasting system.

## Candidate model comparison

The tested candidate models did not outperform the official Logistic Regression model:

- Logistic Regression scaled - World Bank all raw: F1 0.8722
- Random Forest - World Bank all raw: F1 0.8661
- Gradient Boosting - World Bank all raw: F1 0.8585
- Persistence baseline: F1 0.8571
- MLP scaled - World Bank all raw: F1 0.8498

This supports keeping Logistic Regression as the official model due to its better F1-score, interpretability, and methodological simplicity.

## World Bank ablation decision

The best World Bank setup was:

- world_bank_all_raw: F1 0.8722

Engineered feature variants did not improve performance:

- world_bank_wave_1_engineered: F1 0.8711
- world_bank_all_engineered: F1 0.8698
- world_bank_wave_2_engineered: F1 0.8675

Therefore, engineered World Bank features should remain experimental, while raw World Bank indicators remain part of the official pipeline.

## Shock features decision

Shock features did not improve the current official model:

- base_model_replicated: F1 0.8722
- base_plus_shock_features: F1 0.8709
- shock_only_control: F1 0.8404

Therefore, shock features should be documented as an experiment, not adopted into the official model.

## Current technical conclusion

The official project result is:

UCDP Organized Violence + temporal conflict features + raw World Bank indicators + Logistic Regression.

This configuration is currently stronger than:
- UCDP base only;
- UCDP temporal only;
- engineered World Bank variants;
- shock feature variants;
- tested Random Forest, Gradient Boosting, and MLP candidates.

## Methodological caution

The model should not be presented as a direct predictor of world war or as a causal system. It is a supervised country-year classification model estimating next-year conflict risk using historical conflict patterns and socioeconomic indicators.

