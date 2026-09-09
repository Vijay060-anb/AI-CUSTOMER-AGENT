from typing import Dict, Any


# ============================================
# FEEDBACK CONFIGURATION
# ============================================

FEEDBACK_TYPES = [
    "complaint",
    "review",
]


# ============================================
# COMPLAINT
# ============================================

def submit_complaint(
    message: str
) -> Dict[str, Any]:
    """
    Submit a customer complaint.
    """

    if not message.strip():
        return {
            "success": False,
            "message": "Please provide details about your complaint."
        }

    return {
        "success": True,
        "feedback_type": "complaint",
        "status": "submitted",
        "message": (
            "Your complaint has been submitted successfully. "
            "Our customer support team will review it and follow up "
            "if additional information is required."
        ),
    }


# ============================================
# REVIEW
# ============================================

def submit_review(
    message: str
) -> Dict[str, Any]:
    """
    Submit customer feedback/review.
    """

    if not message.strip():
        return {
            "success": False,
            "message": "Please provide your review or feedback."
        }

    return {
        "success": True,
        "feedback_type": "review",
        "status": "submitted",
        "message": (
            "Thank you for your feedback. "
            "Your review has been submitted successfully."
        ),
    }


# ============================================
# TESTS
# ============================================

if __name__ == "__main__":

    print("\n========================================")
    print("FEEDBACK FLOW TESTS")
    print("========================================\n")

    # ----------------------------------------
    # TEST 1
    # ----------------------------------------

    print("1. Submit complaint")

    result = submit_complaint(
        "I am unhappy with the service I received."
    )

    print(result["message"])

    # ----------------------------------------
    # TEST 2
    # ----------------------------------------

    print("\n2. Submit review")

    result = submit_review(
        "The service was excellent and very helpful."
    )

    print(result["message"])

    # ----------------------------------------
    # TEST 3
    # ----------------------------------------

    print("\n3. Empty complaint")

    result = submit_complaint("")

    print(result["message"])

    # ----------------------------------------
    # TEST 4
    # ----------------------------------------

    print("\n4. Empty review")

    result = submit_review("")

    print(result["message"])

    print("\n========================================")
    print("FEEDBACK FLOW TESTS COMPLETE")
    print("========================================")