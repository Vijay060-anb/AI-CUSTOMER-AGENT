from typing import Dict, Any


# ============================================================
# MOCK REFUND DATABASE
# ============================================================

REFUNDS = {
    "10001": {
        "order_id": "10001",
        "refund_eligible": True,
        "refund_status": "not_requested",
        "refund_amount": 79.99,
    },

    "10002": {
        "order_id": "10002",
        "refund_eligible": False,
        "refund_status": "not_eligible",
        "refund_amount": 0.00,
    },

    "10003": {
        "order_id": "10003",
        "refund_eligible": True,
        "refund_status": "processing",
        "refund_amount": 65.00,
    },

    "10004": {
        "order_id": "10004",
        "refund_eligible": True,
        "refund_status": "completed",
        "refund_amount": 39.99,
    },
}


# ============================================================
# REFUND POLICY
# ============================================================

REFUND_POLICY = {
    "standard_period_days": 30,
    "processing_time_days": "3-5 business days",
}


# ============================================================
# GET REFUND INFORMATION
# ============================================================

def get_refund(order_id: str) -> Dict[str, Any]:
    """
    Request a refund for an order.
    """

    refund = REFUNDS.get(order_id)

    if refund is None:
        return {
            "success": False,
            "message": f"Order {order_id} was not found."
        }

    if not refund["refund_eligible"]:
        return {
            "success": False,
            "message": (
                f"Order {order_id} is not eligible "
                "for a refund."
            )
        }

    if refund["refund_status"] == "completed":
        return {
            "success": False,
            "message": (
                f"Refund for order {order_id} "
                "has already been completed."
            )
        }

    if refund["refund_status"] == "processing":
        return {
            "success": False,
            "message": (
                f"Refund for order {order_id} "
                "is already being processed."
            )
        }

    # Request refund
    refund["refund_status"] = "processing"

    return {
        "success": True,
        "message": (
            f"Refund for order {order_id} "
            f"has been requested successfully. "
            f"Refund amount: "
            f"${refund['refund_amount']:.2f}."
        ),
        "order_id": order_id,
        "refund_amount": refund["refund_amount"],
        "refund_status": refund["refund_status"],
    }


# ============================================================
# TRACK REFUND
# ============================================================

def track_refund(order_id: str) -> Dict[str, Any]:
    """
    Check the current status of an order refund.
    """

    refund = REFUNDS.get(order_id)

    if refund is None:
        return {
            "success": False,
            "message": f"Order {order_id} was not found."
        }

    status = refund["refund_status"]

    if status == "not_requested":
        message = (
            f"No refund has been requested "
            f"for order {order_id}."
        )

    elif status == "processing":
        message = (
            f"Refund for order {order_id} "
            "is currently being processed."
        )

    elif status == "completed":
        message = (
            f"Refund for order {order_id} "
            "has been completed."
        )

    elif status == "not_eligible":
        message = (
            f"Order {order_id} is not eligible "
            "for a refund."
        )

    else:
        message = (
            f"Refund status for order {order_id}: "
            f"{status}"
        )

    return {
        "success": True,
        "message": message,
        "order_id": order_id,
        "refund_status": status,
    }


# ============================================================
# CHECK REFUND POLICY
# ============================================================

def check_refund_policy() -> Dict[str, Any]:
    """
    Return the general refund policy.
    """

    days = REFUND_POLICY["standard_period_days"]
    processing_time = REFUND_POLICY["processing_time_days"]

    return {
        "success": True,
        "message": (
            f"Customers can request a refund within "
            f"{days} days of their purchase. "
            f"Refunds typically take "
            f"{processing_time} to process."
        ),
        "standard_period_days": days,
        "processing_time": processing_time,
    }


# ============================================================
# TEST REFUND FLOW
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("REFUND BUSINESS FLOW")
    print("========================================\n")

    # --------------------------------------------------------
    # TEST 1: CHECK POLICY
    # --------------------------------------------------------

    print("TEST 1: Refund policy")

    result = check_refund_policy()

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 2: REQUEST REFUND
    # --------------------------------------------------------

    print("TEST 2: Request refund for order 10001")

    result = get_refund("10001")

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 3: TRACK REFUND
    # --------------------------------------------------------

    print("TEST 3: Track refund for order 10003")

    result = track_refund("10003")

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 4: COMPLETED REFUND
    # --------------------------------------------------------

    print("TEST 4: Track completed refund")

    result = track_refund("10004")

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 5: INELIGIBLE REFUND
    # --------------------------------------------------------

    print("TEST 5: Request refund for ineligible order")

    result = get_refund("10002")

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 6: UNKNOWN ORDER
    # --------------------------------------------------------

    print("TEST 6: Unknown order")

    result = get_refund("99999")

    print(result["message"])

    print("-" * 60)