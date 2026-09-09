from typing import Dict, Any

from agent.smart_router import classify_message
from agent.ai_agent import classify_with_ai


# ============================================================
# HYBRID ROUTER CONFIGURATION
# ============================================================

HIGH_CONFIDENCE = 0.80
MEDIUM_CONFIDENCE = 0.60


# ============================================================
# HYBRID CLASSIFICATION
# ============================================================

def hybrid_classify(message: str) -> Dict[str, Any]:
    """
    Hybrid customer-support router.

    Step 1:
        Use the fast ML classifier.

    Step 2:
        If ML confidence is high (>= 80%),
        use the ML prediction directly.

    Step 3:
        If ML confidence is below 80%,
        send the message to the Groq AI reasoning agent.

    Returns:
        A dictionary containing the final intent,
        confidence, routing method, and AI usage information.
    """

    # --------------------------------------------------------
    # STEP 1: ML CLASSIFIER
    # --------------------------------------------------------

    ml_result = classify_message(message)

    ml_intent = ml_result["intent"]
    ml_confidence = ml_result["confidence"]

    # --------------------------------------------------------
    # STEP 2: HIGH-CONFIDENCE ML ROUTING
    # --------------------------------------------------------

    if ml_confidence >= HIGH_CONFIDENCE:

        return {
            "message": message,

            "final_intent": ml_intent,

            "final_confidence": ml_confidence,

            "routing_method": "ML",

            "routing_action": "AUTO_ROUTE",

            "ml_intent": ml_intent,

            "ml_confidence": ml_confidence,

            "ai_used": False,

            "ai_intent": None,

            "ai_confidence": None,

            "reason": (
                "ML classifier confidence was high, "
                "so the message was automatically routed."
            )
        }

    # --------------------------------------------------------
    # STEP 3: LOW / MEDIUM-CONFIDENCE AI ROUTING
    # --------------------------------------------------------

    ai_result = classify_with_ai(message)

    ai_intent = ai_result["intent"]
    ai_confidence = ai_result["confidence"]

    return {
        "message": message,

        "final_intent": ai_intent,

        "final_confidence": ai_confidence,

        "routing_method": "AI",

        "routing_action": "AI_ROUTE",

        "ml_intent": ml_intent,

        "ml_confidence": ml_confidence,

        "ai_used": True,

        "ai_intent": ai_intent,

        "ai_confidence": ai_confidence,

        "reason": ai_result["reason"]
    }


# ============================================================
# TEST THE HYBRID SYSTEM
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("HYBRID CUSTOMER SUPPORT ROUTER")
    print("========================================\n")

    test_messages = [

        # High-confidence ML example
        "I want to change my shipping address",

        # Low-confidence ML examples
        "Where is my package?",

        "I want to cancel my order",

        "My payment isn't working",

        "I accidentally ordered the wrong item",

        "How long does shipping usually take?",

        "I want to complain about your service",

        "Can I get a refund for this purchase?",
    ]

    for message in test_messages:

        print(f"Customer: {message}")

        try:

            result = hybrid_classify(message)

            print(
                f"ML Intent       : "
                f"{result['ml_intent']}"
            )

            print(
                f"ML Confidence   : "
                f"{result['ml_confidence']:.2%}"
            )

            print(
                f"AI Used         : "
                f"{result['ai_used']}"
            )

            if result["ai_used"]:

                print(
                    f"AI Intent       : "
                    f"{result['ai_intent']}"
                )

                print(
                    f"AI Confidence   : "
                    f"{result['ai_confidence']:.2%}"
                )

            print(
                f"FINAL INTENT    : "
                f"{result['final_intent']}"
            )

            print(
                f"Routing Method  : "
                f"{result['routing_method']}"
            )

            print(
                f"Action          : "
                f"{result['routing_action']}"
            )

            print(
                f"Reason          : "
                f"{result['reason']}"
            )

        except Exception as error:

            print(
                f"ERROR: {error}"
            )

        print("-" * 75)