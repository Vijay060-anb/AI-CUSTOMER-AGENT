from typing import Any, Dict, Optional

from backend.database import (
    get_order as db_get_order,
    update_order,
    create_order,
)


def get_order(order_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve an order from the Supabase database.
    """
    return db_get_order(order_id)


def track_order(order_id: str) -> Dict[str, Any]:
    """
    Track the current status of an order.
    """

    order = get_order(order_id)

    if not order:
        return {
            "success": False,
            "message": "Order not found.",
            "data": None,
        }

    return {
        "success": True,
        "message": (
            f"Order {order_id} is currently "
            f"{order['status']}."
        ),
        "data": order,
    }


def cancel_order(order_id: str) -> Dict[str, Any]:
    """
    Cancel an order if the database says cancellation is allowed.
    """

    order = get_order(order_id)

    if not order:
        return {
            "success": False,
            "message": "Order not found.",
            "data": None,
        }

    if not order["can_cancel"]:
        return {
            "success": False,
            "message": (
                f"Order {order_id} cannot be cancelled "
                f"because it has already been shipped "
                f"or processed."
            ),
            "data": order,
        }

    updated_order = update_order(
        order_id,
        {
            "status": "cancelled",
            "can_cancel": False,
        },
    )

    return {
        "success": True,
        "message": f"Order {order_id} has been cancelled.",
        "data": updated_order,
    }


def change_order(
    order_id: str,
    new_item: str
) -> Dict[str, Any]:
    """
    Change the item in an order if it is still eligible for changes.
    """

    if not new_item:
        return {
            "success": False,
            "message": "Please provide the new item.",
            "data": None,
        }

    order = get_order(order_id)

    if not order:
        return {
            "success": False,
            "message": "Order not found.",
            "data": None,
        }

    if order["status"] != "processing":
        return {
            "success": False,
            "message": (
                f"Order {order_id} cannot be changed "
                f"because it is already {order['status']}."
            ),
            "data": order,
        }

    updated_order = update_order(
        order_id,
        {
            "items": [new_item],
        },
    )

    return {
        "success": True,
        "message": (
            f"Order {order_id} has been changed "
            f"to {new_item}."
        ),
        "data": updated_order,
    }


def place_order(
    customer: str,
    items: list,
    total: float,
    order_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a new order in Supabase.
    """

    if not customer:
        return {
            "success": False,
            "message": "Customer name is required.",
            "data": None,
        }

    if not items:
        return {
            "success": False,
            "message": "At least one item is required.",
            "data": None,
        }

    if total < 0:
        return {
            "success": False,
            "message": "Order total cannot be negative.",
            "data": None,
        }

    if not order_id:
        order_id = "NEW-" + str(
            __import__("time").time_ns()
        )[-8:]

    order = {
        "order_id": order_id,
        "customer": customer,
        "status": "processing",
        "items": items,
        "total": total,
        "can_cancel": True,
    }

    created_order = create_order(order)

    return {
        "success": True,
        "message": (
            f"Order {order_id} has been created successfully."
        ),
        "data": created_order,
    }


if __name__ == "__main__":
    print("Testing Supabase order flow...")
    print()

    result = track_order("10002")

    print("Track order:")
    print(result)