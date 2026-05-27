from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from lightgbm import LGBMClassifier

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay
)

TARGET_COLUMN = "next_month_escalation"

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ============================================================
# OUTPUT PATHS
# ============================================================

MODEL_DIR = PROJECT_ROOT / "models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_PATH = (
    MODEL_DIR /
    "advanced_temporal_conflict_model_wars_deaths.pkl"
)

# ============================================================
# TEMPORAL SPLIT
# ============================================================

def temporal_split(
    df,
    features
):

    print("\nApplying Temporal Split...")

    conflict_order = (

        df.groupby("conflict_id")["year"]

        .min()

        .sort_values()

        .index
    )

    split_position = int(
        len(conflict_order) * 0.80
    )

    train_conflicts = (
        conflict_order[:split_position]
    )

    test_conflicts = (
        conflict_order[split_position:]
    )

    train_df = df[
        df["conflict_id"].isin(
            train_conflicts
        )
    ]

    test_df = df[
        df["conflict_id"].isin(
            test_conflicts
        )
    ]

    X_train = train_df[
        features
    ]

    y_train = train_df[
        TARGET_COLUMN
    ]

    X_test = test_df[
        features
    ]

    y_test = test_df[
        TARGET_COLUMN
    ]

    return (
        X_train,
        X_test,
        y_train,
        y_test
    )

# ============================================================
# TRAIN MODEL
# ============================================================

def train_model(
    X_train,
    y_train
):

    print("\nTraining LightGBM...")

    model = LGBMClassifier(

        n_estimators=500,

        learning_rate=0.03,

        max_depth=6,

        num_leaves=32,

        min_child_samples=50,

        subsample=0.8,

        colsample_bytree=0.8,

        reg_alpha=1.0,

        reg_lambda=1.0,

        random_state=42,

        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    return model

# ============================================================
# THRESHOLD
# ============================================================

def optimize_threshold(
    y_true,
    probabilities
):

    thresholds = np.linspace(
        0.2,
        0.8,
        100
    )

    best_threshold = 0.5
    best_f1 = 0

    for threshold in thresholds:

        preds = (
            probabilities >= threshold
        ).astype(int)

        score = f1_score(
            y_true,
            preds
        )

        if score > best_f1:

            best_f1 = score
            best_threshold = threshold

    return best_threshold

# ============================================================
# EVALUATION
# ============================================================

def evaluate_model(
    model,
    X_test,
    y_test
):

    probs = model.predict_proba(
        X_test
    )[:, 1]

    threshold = optimize_threshold(
        y_test,
        probs
    )

    preds = (
        probs >= threshold
    ).astype(int)

    print("\nModel Metrics:\n")

    print(
        classification_report(
            y_test,
            preds
        )
    )

    matrix = confusion_matrix(
        y_test,
        preds
    )

    fig, ax = plt.subplots(
        figsize=(8, 6)
    )

    disp = ConfusionMatrixDisplay(
        confusion_matrix=matrix
    )

    disp.plot(
        cmap="Blues",
        ax=ax
    )

    plt.tight_layout()

    plt.show()

# ============================================================
# FEATURE IMPORTANCE
# ============================================================

def feature_importance(
    model,
    features
):

    importance_df = pd.DataFrame({

        "feature":
            features,

        "importance":
            model.feature_importances_
    })

    importance_df = (

        importance_df

        .sort_values(
            "importance",
            ascending=False
        )
    )

    print("\nFeature Importance:\n")

    print(importance_df)

# ============================================================
# SAVE MODEL
# ============================================================

def save_model(model):

    joblib.dump(
        model,
        MODEL_PATH
    )

    print("\nModel Saved:")
    print(MODEL_PATH)