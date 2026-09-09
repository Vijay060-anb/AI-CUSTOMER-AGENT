from typing import Dict, Any


# ============================================================
# PAYMENT METHODS
# ============================================================

PAYMENT_METHODS = [
    "Visa",
    "Mastercard",
    "American Express",
    "PayPal",
    "Apple Pay",
]


# ============================================================
# MOCK PAYMENT RECORDS
# ============================================================

PAYMENTS = {
    "10001": {
        "order_id": "10001",
        "payment_method": "Visa",
        "status": "successful",
        "amount": 79.99,
    },
    "10002": {
        "order_id": "10002",
        "payment_method": "PayPal",
        "status": "successful",
        "amount": 45.00,
    },
    "10003": {
        "order_id": "10003",
        "payment_method": "Mastercard",
        "status": "successful",
        "amount": 65.00,
    },
    "10004": {
        "order_id": "10004",
        "payment_method": "Visa",
        "status": "failed",
        "amount": 39.99,
    },
}


# ============================================================
# CHECK PAYMENT METHODS
# ============================================================

def check_payment_methods() -> Dict[str, Any]:
    """
    Return the payment methods currently supported.
    """

    methods = ", ".join(PAYMENT_METHODS)

    return {
        "success": True,
        "message": (
            f"We currently accept: {methods}."
        ),
        "payment_methods": PAYMENT_METHODS,
    }


# ============================================================
# CHECK PAYMENT STATUS
# ============================================================

def check_payment_status(
    order_id: str,
) -> Dict[str, Any]:
    """
    Check the payment status for an order.
    """

    payment = PAYMENTS.get(order_id)

    if payment is None:
        return {
            "success": False,
            "message": (
                f"No payment record was found "
                f"for order {order_id}."
            ),
        }

    return {
        "success": True,
        "message": (
            f"Payment for order {order_id} "
            f"is {payment['status']}."
        ),
        "order_id": order_id,
        "payment_status": payment["status"],
        "payment_method": payment["payment_method"],
        "amount": payment["amount"],
    }


# ============================================================
# HANDLE PAYMENT ISSUE
# ============================================================

def handle_payment_issue(
    order_id: str,
) -> Dict[str, Any]:
    """
    Diagnose a basic payment issue.
    """

    payment = PAYMENTS.get(order_id)

    if payment is None:
        return {
            "success": False,
            "message": (
                f"No payment record was found "
                f"for order {order_id}."
            ),
        }

    if payment["status"] == "successful":

        return {
            "success": True,
            "message": (
                f"The payment for order {order_id} "
                "was successful. If you are still "
                "seeing an error, please contact "
                "customer support."
            ),
            "order_id": order_id,
            "payment_status": "successful",
        }

    if payment["status"] == "failed":

        return {
            "success": False,
            "message": (
                f"The payment for order {order_id} "
                "failed. Please verify your payment "
                "details or try another supported "
                "payment method."
            ),
            "order_id": order_id,
            "payment_status": "failed",
        }

    return {
        "success": False,
        "message": (
            f"The payment for order {order_id} "
            f"is currently {payment['status']}."
        ),
        "order_id": order_id,
        "payment_status": payment["status"],
    }


# ============================================================
# TEST PAYMENT FLOW
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("PAYMENT BUSINESS FLOW")
    print("========================================\n")

    # --------------------------------------------------------
    # TEST 1: PAYMENT METHODS
    # --------------------------------------------------------

    print("TEST 1: Check payment methods")

    result = check_payment_methods()

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 2: SUCCESSFUL PAYMENT
    # --------------------------------------------------------

    print("TEST 2: Check successful payment")

    result = check_payment_status("10001")

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 3: FAILED PAYMENT
    # --------------------------------------------------------

    print("TEST 3: Handle failed payment")

    result = handle_payment_issue("10004")

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 4: SUCCESSFUL PAYMENT ISSUE
    # --------------------------------------------------------

    print("TEST 4: Handle payment issue for successful payment")

    result = handle_payment_issue("10001")

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 5: UNKNOWN ORDER
    # --------------------------------------------------------

    print("TEST 5: Unknown payment record")

    result = handle_payment_issue("99999")

    print(result["message"])

    print("-" * 60)