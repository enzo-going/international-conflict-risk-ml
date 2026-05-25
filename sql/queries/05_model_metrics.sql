-- Model evaluation metrics.

SELECT
    model,
    ROUND(accuracy, 4) AS accuracy,
    ROUND(precision, 4) AS precision,
    ROUND(recall, 4) AS recall,
    ROUND(f1_score, 4) AS f1_score,
    tn,
    fp,
    fn,
    tp,
    ROUND(f1_difference_vs_persistence, 4) AS f1_difference_vs_persistence
FROM model_metrics
ORDER BY f1_score DESC;
