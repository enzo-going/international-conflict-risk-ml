-- Countries and years with the highest predicted conflict risk in the test set.

SELECT
    country,
    year,
    ROUND(y_proba, 4) AS predicted_risk,
    y_true,
    y_pred
FROM model_predictions
ORDER BY y_proba DESC
LIMIT 20;
