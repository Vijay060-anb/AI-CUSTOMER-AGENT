from typing import Dict, Any


# ============================================
# CANCELLATION CONFIGURATION
# ============================================

CANCELLATION_POLICY = {
    "fee": 0.00,
    "currency": "USD",
    "condition": "Orders can be cancelled before shipment."
}


# ============================================
# CHECK CANCELLATION FEE
# ============================================

def check_cancellation_fee() -> Dict[str, Any]:
    """
    Return the current cancellation fee and policy.
    """

    return {
        "success": True,
        "fee": CANCELLATION_POLICY["fee"],
        "currency": CANCELLATION_POLICY["currency"],
        "condition": CANCELLATION_POLICY["condition"],
        "message": (
            "There is currently no cancellation fee. "
            "Orders can be cancelled before they are shipped."
        ),
    }


# ============================================
# TESTS
# ============================================

if __name__ == "__main__":

    print("\n========================================")
    print("CANCELLATION FLOW TESTS")
    print("========================================\n")

    print("1. Check cancellation fee")

    result = check_cancellation_fee()

    print(result["message"])

    print("\n2. Cancellation fee amount")

    print(
        "Fee:",
        result["fee"],
        result["currency"]
    )

    print("\n3. Cancellation condition")

    print(result["condition"])

    print("\n========================================")
    print("CANCELLATION FLOW TESTS COMPLETE")
    print("========================================")