-- Candidate model comparison ordered by F1-score.

SELECT
    model,
    feature_count,
    ROUND(accuracy, 4) AS accuracy,
    ROUND(precision, 4) AS precision,
    ROUND(recall, 4) AS recall,
    ROUND(f1_score, 4) AS f1_score,
    tn,
    fp,
    fn,
    tp,
    ROUND(f1_difference_vs_persistence, 4) AS f1_difference_vs_persistence
FROM candidate_model_comparison
ORDER BY f1_score DESC;
