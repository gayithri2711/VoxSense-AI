
from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "features.csv"
MODEL_DIR = PROJECT_DIR / "models"
MODEL_FILE = MODEL_DIR / "emotion_model.joblib"

def main():
    if not DATA_FILE.exists():
        print(f"Features file not found: {DATA_FILE}")
        print("Run extract_features.py first.")
        return

    df = pd.read_csv(DATA_FILE)

    feature_columns = [
        column for column in df.columns
        if column.startswith("mfcc_")
    ]

    if not feature_columns or "emotion" not in df or "actor" not in df:
        print("The CSV is missing required feature, emotion, or actor columns.")
        return

    X = df[feature_columns]
    y = df["emotion"]
    groups = df["actor"]

    # Keep actors separate between training and testing.
    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.25,
        random_state=42
    )
    train_idx, test_idx = next(splitter.split(X, y, groups))

    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    model = make_pipeline(
        StandardScaler(),
        SVC(kernel="rbf", probability=True, class_weight="balanced",
            random_state=42)
    )

    print(f"Training recordings: {len(X_train)}")
    print(f"Testing recordings: {len(X_test)}")
    print("\nTraining model...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"\nTest accuracy: {accuracy:.1%}")
    print("\nClassification report:")
    print(classification_report(
        y_test,
        predictions,
        zero_division=0
    ))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        {
            "model": model,
            "feature_columns": feature_columns,
            "emotions": sorted(y.unique().tolist()),
        },
        MODEL_FILE
    )

    print(f"\nModel saved to: {MODEL_FILE}")

if __name__ == "__main__":
    main()
