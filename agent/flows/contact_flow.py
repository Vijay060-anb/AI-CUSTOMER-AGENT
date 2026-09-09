from typing import Dict, Any


# ============================================
# CONTACT / SUPPORT CONFIGURATION
# ============================================

SUPPORT_CHANNELS = [
    "Live Chat",
    "Email",
    "Phone",
]

SUPPORT_HOURS = {
    "days": "Monday-Friday",
    "hours": "09:00-18:00",
    "timezone": "CET",
}


# ============================================
# CONTACT CUSTOMER SERVICE
# ============================================

def contact_customer_service() -> Dict[str, Any]:
    """
    Provide available customer-service contact options.
    """

    return {
        "success": True,
        "channels": SUPPORT_CHANNELS,
        "support_hours": SUPPORT_HOURS,
        "message": (
            "You can contact customer service through Live Chat, "
            "Email, or Phone. Customer service is available "
            "Monday-Friday from 09:00 to 18:00 CET."
        ),
    }


# ============================================
# CONTACT HUMAN AGENT
# ============================================

def contact_human_agent() -> Dict[str, Any]:
    """
    Escalate the customer request to a human support agent.
    """

    return {
        "success": True,
        "escalated": True,
        "priority": "normal",
        "message": (
            "Your request has been escalated to a human support agent. "
            "A support representative will assist you shortly."
        ),
    }


# ============================================
# TESTS
# ============================================

if __name__ == "__main__":

    print("\n========================================")
    print("CONTACT FLOW TESTS")
    print("========================================\n")

    # ----------------------------------------
    # TEST 1
    # ----------------------------------------

    print("1. Contact customer service")

    result = contact_customer_service()

    print(result["message"])

    # ----------------------------------------
    # TEST 2
    # ----------------------------------------

    print("\n2. Contact human agent")

    result = contact_human_agent()

    print(result["message"])

    # ----------------------------------------
    # TEST 3
    # ----------------------------------------

    print("\n3. Customer service channels")

    result = contact_customer_service()

    print("Channels:", ", ".join(result["channels"]))

    # ----------------------------------------
    # TEST 4
    # ----------------------------------------

    print("\n4. Support hours")

    result = contact_customer_service()

    print(
        "Hours:",
        result["support_hours"]["days"],
        result["support_hours"]["hours"],
        result["support_hours"]["timezone"],
    )

    print("\n========================================")
    print("CONTACT FLOW TESTS COMPLETE")
    print("========================================")