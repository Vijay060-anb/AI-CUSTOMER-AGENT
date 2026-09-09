from typing import Dict, Any


# ============================================
# SUBSCRIPTION CONFIGURATION
# ============================================

SUBSCRIPTION = {
    "name": "Newsletter",
    "status": "active",
    "frequency": "weekly",
}


# ============================================
# NEWSLETTER SUBSCRIPTION
# ============================================

def manage_newsletter_subscription(
    action: str = "status"
) -> Dict[str, Any]:
    """
    Manage newsletter subscription.

    Supported actions:
    - subscribe
    - unsubscribe
    - status
    """

    action = action.lower().strip()

    if action == "subscribe":

        SUBSCRIPTION["status"] = "active"

        return {
            "success": True,
            "status": "active",
            "message": (
                "You have been successfully subscribed "
                "to our weekly newsletter."
            ),
        }

    elif action == "unsubscribe":

        SUBSCRIPTION["status"] = "inactive"

        return {
            "success": True,
            "status": "inactive",
            "message": (
                "You have been successfully unsubscribed "
                "from our newsletter."
            ),
        }

    elif action == "status":

        status = SUBSCRIPTION["status"]

        if status == "active":
            message = (
                "Your newsletter subscription is currently active. "
                "You receive the newsletter weekly."
            )
        else:
            message = (
                "Your newsletter subscription is currently inactive."
            )

        return {
            "success": True,
            "status": status,
            "message": message,
        }

    return {
        "success": False,
        "message": (
            "Invalid subscription action. "
            "Supported actions are subscribe, unsubscribe, and status."
        ),
    }


# ============================================
# TESTS
# ============================================

if __name__ == "__main__":

    print("\n========================================")
    print("SUBSCRIPTION FLOW TESTS")
    print("========================================\n")

    print("1. Check subscription status")

    result = manage_newsletter_subscription("status")

    print(result["message"])

    print("\n2. Unsubscribe")

    result = manage_newsletter_subscription("unsubscribe")

    print(result["message"])

    print("\n3. Check status after unsubscribe")

    result = manage_newsletter_subscription("status")

    print(result["message"])

    print("\n4. Subscribe again")

    result = manage_newsletter_subscription("subscribe")

    print(result["message"])

    print("\n5. Check status after subscribing")

    result = manage_newsletter_subscription("status")

    print(result["message"])

    print("\n6. Invalid action")

    result = manage_newsletter_subscription("invalid")

    print(result["message"])

    print("\n========================================")
    print("SUBSCRIPTION FLOW TESTS COMPLETE")
    print("========================================")