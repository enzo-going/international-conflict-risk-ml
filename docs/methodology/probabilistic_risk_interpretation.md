# Probabilistic Risk Interpretation

## Purpose

This document consolidates the interpretation of the probabilistic outputs produced by the current official conflict risk model.

The model should be interpreted as a country-year risk classification system, not as a deterministic forecasting system.

## Official probability output

The official model generates a predicted probability for `target_conflict_next_year`.

Current test scope:

- Test period: 2017-2023
- Unit: country-year
- Number of test cases: 1358
- Number of countries: 194
- Model: Logistic Regression scaled - World Bank all raw
- Features: 33

## Threshold decision

The best threshold by F1-score is currently:

- Threshold: 0.50
- Accuracy: 0.9197
- Precision: 0.9029
- Recall: 0.8435
- F1-score: 0.8722
- True negatives: 877
- False positives: 40
- False negatives: 69
- True positives: 372

This supports using 0.50 as the official classification threshold.

## Alternative threshold interpretation

Lower thresholds increase recall but reduce precision.

For example:

- Threshold 0.40: precision 0.8702, recall 0.8662, F1 0.8682
- Threshold 0.30: precision 0.8387, recall 0.8844, F1 0.8609
- Threshold 0.20: precision 0.7968, recall 0.9161, F1 0.8523

This means that lower thresholds can be useful for exploratory early-warning analysis, but they should not replace the official threshold unless the project explicitly prioritizes recall over precision.

## Calibration interpretation

The calibration analysis suggests that the model is more reliable at the extreme probability ranges than in the middle probability bands.

Important observations:

- The 0.9-1.0 bin has mean predicted probability 0.9831 and observed positive rate 0.9863.
- The 0.0-0.1 bin has mean predicted probability 0.0417 and observed positive rate 0.0203.
- Middle bins contain fewer samples and show larger calibration errors.

Therefore, probability bands should be interpreted cautiously, especially in moderate-risk ranges.

## Risk band summary

For the latest country risk assessment:

- Forecast year: 2024
- Countries evaluated: 194
- Mean probability: 0.3427
- Median probability: 0.0932
- High or very high risk countries: 59
- Predicted positive countries: 60
- Actual positive countries: 58

Risk level distribution:

- Very low: 120 countries
- Low: 11 countries
- Moderate: 4 countries
- High: 5 countries
- Very high: 54 countries

## Methodological caution

The risk scores should not be interpreted as deterministic predictions.

They represent estimated probabilities based on historical conflict patterns, temporal features, and socioeconomic indicators. The model is useful for comparative risk analysis and academic exploration, but it should not be presented as an operational geopolitical forecasting system.

## Current conclusion

The probabilistic layer strengthens the project because it allows the model to be interpreted beyond a binary classification.

The strongest presentation is:

UCDP Organized Violence + temporal conflict features + raw World Bank indicators + Logistic Regression + probabilistic risk assessment.

This framing supports:
- classification performance;
- threshold analysis;
- risk band interpretation;
- country-level risk ranking;
- cautious academic discussion.

