from pathlib import Path

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "final"
    / "conflict_ml_features.csv"
)

MODEL_OUTPUT_PATH = (
    PROJECT_ROOT
    / "models"
    / "conflict_escalation_model.pkl"
)


TARGET_COLUMN = "future_conflict_escalation"


FEATURE_COLUMNS = [
    "total_deaths",
    "previous_year_deaths",
    "death_growth_rate",
    "rolling_mean_deaths_3y",
    "rolling_max_deaths_3y",
    "conflict_duration_years",
    "cumulative_deaths",
    "conflict_momentum",
]


def load_dataset() -> pd.DataFrame:
    """Load feature engineered dataset."""

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_PATH}"
        )

    return pd.read_csv(INPUT_PATH)


def validate_columns(df: pd.DataFrame) -> None:
    """Validate required columns."""

    required_columns = FEATURE_COLUMNS + [
        TARGET_COLUMN
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


def prepare_training_data(
    df: pd.DataFrame,
):
    """
    Prepare training features and target.
    """

    dataset = df.copy()

    X = dataset[FEATURE_COLUMNS]

    y = dataset[TARGET_COLUMN]

    return X, y


def split_dataset(
    X,
    y,
):
    """
    Create train/test split.

    shuffle=False preserves temporal order.
    """

    return train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False,
    )


def train_model(
    X_train,
    y_train,
) -> RandomForestClassifier:
    """
    Train Random Forest model.
    """

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
    )

    model.fit(X_train, y_train)

    return model


def evaluate_model(
    model,
    X_test,
    y_test,
) -> None:
    """
    Evaluate trained model.
    """

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    f1 = f1_score(
        y_test,
        predictions,
    )

    print()
    print("MODEL EVALUATION")
    print("----------------")

    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")

    print()
    print("Classification Report:")

    print(
        classification_report(
            y_test,
            predictions,
        )
    )

    print()
    print("Confusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            predictions,
        )
    )


def print_feature_importance(
    model,
) -> None:
    """
    Print feature importance.
    """

    importance_df = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "importance": model.feature_importances_,
        }
    )

    importance_df = importance_df.sort_values(
        "importance",
        ascending=False,
    )

    print()
    print("FEATURE IMPORTANCE")
    print("------------------")

    for _, row in importance_df.iterrows():
        print(
            f"{row['feature']}: "
            f"{row['importance']:.4f}"
        )


def main() -> None:
    dataset = load_dataset()

    validate_columns(dataset)

    X, y = prepare_training_data(
        dataset
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = split_dataset(X, y)

    model = train_model(
        X_train,
        y_train,
    )

    evaluate_model(
        model,
        X_test,
        y_test,
    )

    print_feature_importance(
        model
    )


if __name__ == "__main__":
    main()