from pathlib import Path
from typing import List, Optional
import json


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INTENT_MAP_FILE = PROJECT_ROOT / "agent" / "intent_map.json"


# ============================================================
# LOAD INTENT MAP
# ============================================================

with open(INTENT_MAP_FILE, "r", encoding="utf-8") as file:
    INTENT_MAP = json.load(file)


# ============================================================
# FIND CATEGORY
# ============================================================

def find_category(intent: str) -> Optional[str]:
    """
    Return the category associated with an intent.
    """

    for category, intents in INTENT_MAP.items():

        if intent in intents:
            return category

    return None


# ============================================================
# LIST ALL INTENTS
# ============================================================

def list_intents() -> List[str]:
    """
    Return all available intents.
    """

    intents = []

    for category_intents in INTENT_MAP.values():
        intents.extend(category_intents)

    return sorted(intents)


# ============================================================
# TEST ROUTER
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("AI CUSTOMER SUPPORT INTENT ROUTER")
    print("========================================\n")

    print("Categories:")

    for category, intents in INTENT_MAP.items():

        print(f"\n{category}")

        for intent in intents:
            print(f"  - {intent}")

    print("\n========================================")
    print("ROUTER SUMMARY")
    print("========================================")

    print(f"\nTotal categories: {len(INTENT_MAP)}")
    print(f"Total intents: {len(list_intents())}")

    print("\nExample routing:")

    print(
        "cancel_order ->",
        find_category("cancel_order")
    )

    print(
        "get_refund ->",
        find_category("get_refund")
    )

    print(
        "track_order ->",
        find_category("track_order")
    )

    print(
        "payment_issue ->",
        find_category("payment_issue")
    )

    print(
        "unknown_intent ->",
        find_category("unknown_intent")
    )

    print("\n========================================")
    print("ROUTER TEST COMPLETE")
    print("========================================\n")