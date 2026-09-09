from typing import Dict, Any


# ============================================
# MOCK INVOICE DATA
# ============================================

INVOICES = {
    "10001": {
        "order_id": "10001",
        "invoice_id": "INV-10001",
        "status": "available",
        "amount": 79.99,
        "currency": "USD",
    },
    "10002": {
        "order_id": "10002",
        "invoice_id": "INV-10002",
        "status": "available",
        "amount": 45.00,
        "currency": "USD",
    },
    "10003": {
        "order_id": "10003",
        "invoice_id": "INV-10003",
        "status": "available",
        "amount": 65.00,
        "currency": "USD",
    },
    "10004": {
        "order_id": "10004",
        "invoice_id": "INV-10004",
        "status": "available",
        "amount": 39.99,
        "currency": "USD",
    },
}


# ============================================
# CHECK INVOICE
# ============================================

def check_invoice(order_id: str) -> Dict[str, Any]:
    """
    Check invoice information for an order.
    """

    if order_id not in INVOICES:
        return {
            "success": False,
            "message": f"No invoice was found for order {order_id}."
        }

    invoice = INVOICES[order_id]

    return {
        "success": True,
        "order_id": order_id,
        "invoice_id": invoice["invoice_id"],
        "status": invoice["status"],
        "amount": invoice["amount"],
        "currency": invoice["currency"],
        "message": (
            f"Invoice {invoice['invoice_id']} for order {order_id} "
            f"is {invoice['status']}. "
            f"Total amount: {invoice['amount']:.2f} "
            f"{invoice['currency']}."
        ),
    }


# ============================================
# GET INVOICE
# ============================================

def get_invoice(order_id: str) -> Dict[str, Any]:
    """
    Retrieve an invoice for an order.
    """

    if order_id not in INVOICES:
        return {
            "success": False,
            "message": f"No invoice was found for order {order_id}."
        }

    invoice = INVOICES[order_id]

    if invoice["status"] != "available":
        return {
            "success": False,
            "message": (
                f"Invoice {invoice['invoice_id']} "
                "is not currently available."
            )
        }

    return {
        "success": True,
        "order_id": order_id,
        "invoice_id": invoice["invoice_id"],
        "status": "available",
        "download_available": True,
        "message": (
            f"Invoice {invoice['invoice_id']} is available "
            f"for order {order_id}. "
            "The invoice is ready to download."
        ),
    }


# ============================================
# TESTS
# ============================================

if __name__ == "__main__":

    print("\n========================================")
    print("INVOICE FLOW TESTS")
    print("========================================\n")

    print("1. Check invoice")

    result = check_invoice("10001")

    print(result["message"])

    print("\n2. Get invoice")

    result = get_invoice("10001")

    print(result["message"])

    print("\n3. Check invoice - another order")

    result = check_invoice("10003")

    print(result["message"])

    print("\n4. Get invoice - another order")

    result = get_invoice("10004")

    print(result["message"])

    print("\n5. Unknown invoice")

    result = check_invoice("99999")

    print(result["message"])

    print("\n6. Unknown invoice download")

    result = get_invoice("99999")

    print(result["message"])

    print("\n========================================")
    print("INVOICE FLOW TESTS COMPLETE")
    print("========================================")