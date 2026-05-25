-- Most influential model features by absolute logistic regression coefficient.

SELECT
    rank,
    feature,
    feature_group,
    ROUND(coefficient, 4) AS coefficient,
    ROUND(absolute_coefficient, 4) AS absolute_coefficient,
    effect
FROM model_coefficients
ORDER BY absolute_coefficient DESC
LIMIT 20;
