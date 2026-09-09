from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "intent_classifier.joblib"
)

TEST_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "real_world_test.csv"
)


# ============================================================
# LOAD MODEL
# ============================================================

print("\n========================================")
print("REAL-WORLD CUSTOMER MESSAGE EVALUATION")
print("========================================\n")

print("Loading model...")

model = joblib.load(MODEL_FILE)

print("Model loaded successfully.")


# ============================================================
# LOAD TEST DATA
# ============================================================

df = pd.read_csv(TEST_FILE)

print(f"\nReal-world test messages: {len(df)}")


# ============================================================
# PREDICTIONS
# ============================================================

predictions = []
confidences = []

for message in df["message"]:

    probabilities = model.predict_proba([message])[0]

    best_index = probabilities.argmax()

    prediction = model.classes_[best_index]

    confidence = probabilities[best_index]

    predictions.append(prediction)
    confidences.append(confidence)


df["predicted_intent"] = predictions
df["confidence"] = confidences


# ============================================================
# RESULTS
# ============================================================

df["correct"] = (
    df["expected_intent"]
    == df["predicted_intent"]
)


accuracy = accuracy_score(
    df["expected_intent"],
    df["predicted_intent"],
)


print("\n========================================")
print("RESULT")
print("========================================\n")

print(f"Accuracy: {accuracy:.2%}")

print(
    f"Correct: "
    f"{df['correct'].sum()} / {len(df)}"
)


# ============================================================
# SHOW EVERY PREDICTION
# ============================================================

print("\n========================================")
print("PREDICTIONS")
print("========================================\n")


for _, row in df.iterrows():

    status = "✓" if row["correct"] else "✗"

    print(status, row["message"])

    print(
        f"Expected : {row['expected_intent']}"
    )

    print(
        f"Predicted: {row['predicted_intent']}"
    )

    print(
        f"Confidence: {row['confidence']:.2%}"
    )

    print("-" * 70)


# ============================================================
# WRONG PREDICTIONS
# ============================================================

wrong = df[~df["correct"]]


print("\n========================================")
print("WRONG PREDICTIONS")
print("========================================\n")


if len(wrong) == 0:

    print("No incorrect predictions.")

else:

    for _, row in wrong.iterrows():

        print(f"Message: {row['message']}")
        print(f"Expected: {row['expected_intent']}")
        print(f"Predicted: {row['predicted_intent']}")
        print(f"Confidence: {row['confidence']:.2%}")
        print("-" * 70)


# ============================================================
# LOW CONFIDENCE
# ============================================================

low_confidence = df[
    df["confidence"] < 0.70
]


print("\n========================================")
print("LOW-CONFIDENCE PREDICTIONS")
print("========================================\n")

print(
    f"Messages below 70% confidence: "
    f"{len(low_confidence)}"
)


for _, row in low_confidence.iterrows():

    print(
        f"{row['confidence']:.2%} | "
        f"{row['predicted_intent']} | "
        f"{row['message']}"
    )


# ============================================================
# SAVE RESULTS
# ============================================================

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "real_world_results.csv"
)

df.to_csv(
    OUTPUT_FILE,
    index=False,
)


print("\n========================================")
print("EVALUATION SAVED")
print("========================================\n")

print(OUTPUT_FILE)