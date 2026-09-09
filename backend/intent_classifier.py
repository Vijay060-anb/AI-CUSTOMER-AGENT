from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.pipeline import Pipeline


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TRAIN_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "train.csv"
)

VALIDATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "validation.csv"
)

TEST_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "test.csv"
)

MODEL_DIR = PROJECT_ROOT / "models"

MODEL_FILE = MODEL_DIR / "intent_classifier.joblib"


# ============================================================
# SETTINGS
# ============================================================

RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

print("\n========================================")
print("AI CUSTOMER SUPPORT INTENT CLASSIFIER")
print("========================================\n")

print("Loading datasets...")

train_df = pd.read_csv(TRAIN_FILE)
validation_df = pd.read_csv(VALIDATION_FILE)
test_df = pd.read_csv(TEST_FILE)

print(f"Training records   : {len(train_df):,}")
print(f"Validation records : {len(validation_df):,}")
print(f"Test records       : {len(test_df):,}")


# ============================================================
# FEATURES AND TARGET
# ============================================================

X_train = train_df["instruction"]
y_train = train_df["intent"]

X_validation = validation_df["instruction"]
y_validation = validation_df["intent"]

X_test = test_df["instruction"]
y_test = test_df["intent"]


# ============================================================
# CREATE PIPELINE
# ============================================================

print("\nCreating TF-IDF + Logistic Regression pipeline...")


model = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.98,
                sublinear_tf=True,
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000,
                random_state=RANDOM_STATE,
            ),
        ),
    ]
)


# ============================================================
# TRAIN
# ============================================================

print("\nTraining classifier...")

model.fit(
    X_train,
    y_train,
)

print("Training complete.")


# ============================================================
# VALIDATION
# ============================================================

print("\n========================================")
print("VALIDATION")
print("========================================\n")

validation_predictions = model.predict(
    X_validation
)

validation_accuracy = accuracy_score(
    y_validation,
    validation_predictions,
)

print(
    f"Validation accuracy: "
    f"{validation_accuracy:.4f}"
)

print(
    f"Validation accuracy: "
    f"{validation_accuracy * 100:.2f}%"
)


# ============================================================
# FINAL TEST
# ============================================================

print("\n========================================")
print("FINAL TEST")
print("========================================\n")

test_predictions = model.predict(
    X_test
)

test_accuracy = accuracy_score(
    y_test,
    test_predictions,
)

print(
    f"Test accuracy: "
    f"{test_accuracy:.4f}"
)

print(
    f"Test accuracy: "
    f"{test_accuracy * 100:.2f}%"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\n========================================")
print("CLASSIFICATION REPORT")
print("========================================\n")

report = classification_report(
    y_test,
    test_predictions,
    zero_division=0,
)

print(report)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print("\n========================================")
print("CONFUSION MATRIX")
print("========================================\n")

labels = sorted(
    y_test.unique()
)

matrix = confusion_matrix(
    y_test,
    test_predictions,
    labels=labels,
)

matrix_df = pd.DataFrame(
    matrix,
    index=labels,
    columns=labels,
)

print(matrix_df)


# ============================================================
# SAVE MODEL
# ============================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

joblib.dump(
    model,
    MODEL_FILE,
)

print("\n========================================")
print("MODEL SAVED")
print("========================================\n")

print(MODEL_FILE)


# ============================================================
# SAMPLE PREDICTIONS
# ============================================================

print("\n========================================")
print("SAMPLE PREDICTIONS")
print("========================================\n")


sample_messages = [
    "I want to cancel my order",
    "Where is my refund?",
    "I forgot my password",
    "What payment methods do you accept?",
    "How can I track my package?",
    "I want to change my shipping address",
]


for message in sample_messages:

    prediction = model.predict(
        [message]
    )[0]

    probabilities = model.predict_proba(
        [message]
    )[0]

    confidence = probabilities.max()

    print(f"Customer : {message}")
    print(f"Intent   : {prediction}")
    print(f"Confidence: {confidence:.2%}")
    print("-" * 60)


print("\n========================================")
print("CLASSIFIER COMPLETE")
print("========================================\n") @