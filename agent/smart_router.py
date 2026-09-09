from pathlib import Path
from typing import Dict, Any

import joblib


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "intent_classifier.joblib"
)


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_FILE)


# ============================================================
# CONFIDENCE THRESHOLDS
# ============================================================

HIGH_CONFIDENCE = 0.80
MEDIUM_CONFIDENCE = 0.60


# ============================================================
# CLASSIFY MESSAGE
# ============================================================

def classify_message(message: str) -> Dict[str, Any]:
    """
    Classify a customer message and determine
    whether it is safe to route automatically.
    """

    probabilities = model.predict_proba([message])[0]

    best_index = probabilities.argmax()

    intent = model.classes_[best_index]

    confidence = float(probabilities[best_index])


    # Determine confidence level

    if confidence >= HIGH_CONFIDENCE:
        confidence_level = "HIGH"
        action = "AUTO_ROUTE"

    elif confidence >= MEDIUM_CONFIDENCE:
        confidence_level = "MEDIUM"
        action = "VERIFY"

    else:
        confidence_level = "LOW"
        action = "AI_AGENT"


    return {
        "message": message,
        "intent": intent,
        "confidence": confidence,
        "confidence_percent": round(
            confidence * 100,
            2
        ),
        "confidence_level": confidence_level,
        "action": action,
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("SMART CUSTOMER SUPPORT ROUTER")
    print("========================================\n")


    test_messages = [
        "I want to change my shipping address",
        "Where is my package?",
        "I want to cancel my order",
        "My payment isn't working",
        "I want to speak with a human",
    ]


    for message in test_messages:

        result = classify_message(message)

        print(f"Customer : {result['message']}")
        print(f"Intent   : {result['intent']}")
        print(
            f"Confidence: "
            f"{result['confidence_percent']:.2f}%"
        )
        print(
            f"Level    : "
            f"{result['confidence_level']}"
        )
        print(
            f"Action   : "
            f"{result['action']}"
        )

        print("-" * 70)