from typing import Dict, Any


# ============================================
# MOCK SHIPPING DATA
# ============================================

SHIPPING_ADDRESSES = {
    "10001": {
        "order_id": "10001",
        "customer": "Alex",
        "address": "12 Main Street, Paris",
        "can_change": True,
    },
    "10002": {
        "order_id": "10002",
        "customer": "Maria",
        "address": "45 River Road, Lyon",
        "can_change": False,
    },
    "10003": {
        "order_id": "10003",
        "customer": "John",
        "address": "8 Garden Avenue, Marseille",
        "can_change": False,
    },
    "10004": {
        "order_id": "10004",
        "customer": "Emma",
        "address": "21 Central Street, Nice",
        "can_change": True,
    },
}


DELIVERY_OPTIONS = [
    {
        "name": "Standard Delivery",
        "price": 0.00,
        "estimated_days": "5-7 business days",
    },
    {
        "name": "Express Delivery",
        "price": 9.99,
        "estimated_days": "2-3 business days",
    },
    {
        "name": "Next-Day Delivery",
        "price": 19.99,
        "estimated_days": "1 business day",
    },
]


DELIVERY_PERIOD = {
    "standard": "5-7 business days",
    "express": "2-3 business days",
    "next_day": "1 business day",
}


# ============================================
# DELIVERY FUNCTIONS
# ============================================

def get_delivery_options() -> Dict[str, Any]:
    """
    Return the available delivery options.
    """

    return {
        "success": True,
        "options": DELIVERY_OPTIONS,
        "message": (
            "Available delivery options: "
            "Standard Delivery (free, 5-7 business days), "
            "Express Delivery ($9.99, 2-3 business days), "
            "Next-Day Delivery ($19.99, 1 business day)."
        ),
    }


def get_delivery_period() -> Dict[str, Any]:
    """
    Return standard delivery time.
    """

    return {
        "success": True,
        "standard_delivery": DELIVERY_PERIOD["standard"],
        "express_delivery": DELIVERY_PERIOD["express"],
        "next_day_delivery": DELIVERY_PERIOD["next_day"],
        "message": (
            "Standard delivery takes 5-7 business days. "
            "Express delivery takes 2-3 business days. "
            "Next-Day delivery takes 1 business day."
        ),
    }


def change_shipping_address(
    order_id: str,
    new_address: str
) -> Dict[str, Any]:
    """
    Change the shipping address for an order.
    """

    if order_id not in SHIPPING_ADDRESSES:
        return {
            "success": False,
            "message": f"Order {order_id} was not found."
        }

    order = SHIPPING_ADDRESSES[order_id]

    if not order["can_change"]:
        return {
            "success": False,
            "message": (
                f"The shipping address for order {order_id} "
                "cannot be changed because the order has already been shipped."
            )
        }

    if not new_address.strip():
        return {
            "success": False,
            "message": "Please provide the new shipping address."
        }

    old_address = order["address"]
    order["address"] = new_address

    return {
        "success": True,
        "order_id": order_id,
        "old_address": old_address,
        "new_address": new_address,
        "message": (
            f"The shipping address for order {order_id} "
            "has been successfully updated."
        ),
    }


def set_up_shipping_address(
    order_id: str,
    address: str
) -> Dict[str, Any]:
    """
    Set a shipping address for an order.
    """

    if order_id not in SHIPPING_ADDRESSES:
        return {
            "success": False,
            "message": f"Order {order_id} was not found."
        }

    if not address.strip():
        return {
            "success": False,
            "message": "Please provide a shipping address."
        }

    SHIPPING_ADDRESSES[order_id]["address"] = address

    return {
        "success": True,
        "order_id": order_id,
        "address": address,
        "message": (
            f"Shipping address for order {order_id} "
            "has been set successfully."
        ),
    }


# ============================================
# TESTS
# ============================================

if __name__ == "__main__":

    print("\n========================================")
    print("SHIPPING FLOW TESTS")
    print("========================================\n")

    # ----------------------------------------
    # TEST 1
    # ----------------------------------------

    print("1. Delivery options")

    result = get_delivery_options()

    print(result["message"])

    # ----------------------------------------
    # TEST 2
    # ----------------------------------------

    print("\n2. Delivery period")

    result = get_delivery_period()

    print(result["message"])

    # ----------------------------------------
    # TEST 3
    # ----------------------------------------

    print("\n3. Change shipping address")

    result = change_shipping_address(
        "10001",
        "99 New Street, Paris"
    )

    print(result["message"])

    # ----------------------------------------
    # TEST 4
    # ----------------------------------------

    print("\n4. Change address for shipped order")

    result = change_shipping_address(
        "10002",
        "100 New Road, Lyon"
    )

    print(result["message"])

    # ----------------------------------------
    # TEST 5
    # ----------------------------------------

    print("\n5. Set up shipping address")

    result = set_up_shipping_address(
        "10004",
        "55 Example Street, Nice"
    )

    print(result["message"])

    # ----------------------------------------
    # TEST 6
    # ----------------------------------------

    print("\n6. Unknown order")

    result = change_shipping_address(
        "99999",
        "10 Test Street, Paris"
    )

    print(result["message"])

    # ----------------------------------------
    # TEST 7
    # ----------------------------------------

    print("\n7. Missing address")

    result = set_up_shipping_address(
        "10001",
        ""
    )

    print(result["message"])

    print("\n========================================")
    print("SHIPPING FLOW TESTS COMPLETE")
    print("========================================")