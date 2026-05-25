-- False positives: cases where the model predicted conflict, but the actual label was 0.

SELECT
    country,
    year,
    ROUND(y_proba, 4) AS predicted_risk,
    y_true,
    y_pred
FROM model_predictions
WHERE y_true = 0
  AND y_pred = 1
ORDER BY y_proba DESC;
