-- False negatives: cases where the model predicted no conflict, but the actual label was 1.

SELECT
    country,
    year,
    ROUND(y_proba, 4) AS predicted_risk,
    y_true,
    y_pred
FROM model_predictions
WHERE y_true = 1
  AND y_pred = 0
ORDER BY y_proba ASC;
