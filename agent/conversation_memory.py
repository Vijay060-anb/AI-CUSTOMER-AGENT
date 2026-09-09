from typing import Dict, List, Any
import re


# =========================================================
# CONVERSATION STORAGE
# =========================================================

_conversations: Dict[
    str,
    List[Dict[str, Any]]
] = {}


# =========================================================
# ADD MESSAGE
# =========================================================

def add_message(
    conversation_id: str,
    role: str,
    message: str,
) -> None:

    if not conversation_id:
        return

    if conversation_id not in _conversations:
        _conversations[conversation_id] = []

    _conversations[conversation_id].append(
        {
            "role": role,
            "message": message,
        }
    )


# =========================================================
# GET HISTORY
# =========================================================

def get_history(
    conversation_id: str,
) -> List[Dict[str, Any]]:

    if not conversation_id:
        return []

    return _conversations.get(
        conversation_id,
        []
    )


# =========================================================
# EXTRACT ORDER ID
# =========================================================

def extract_order_id(
    message: str
) -> str:

    match = re.search(
        r"\b\d{4,}\b",
        message
    )

    if match:
        return match.group(0)

    return ""


# =========================================================
# GET PREVIOUS ORDER ID
# =========================================================

def get_previous_order_id(
    conversation_id: str
) -> str:

    history = get_history(
        conversation_id
    )

    for item in reversed(history):

        if item.get("role") != "user":
            continue

        message = item.get(
            "message",
            ""
        )

        order_id = extract_order_id(
            message
        )

        if order_id:
            return order_id

    return ""


# =========================================================
# GET LAST USER MESSAGE
# =========================================================

def get_last_user_message(
    conversation_id: str
) -> str:

    history = get_history(
        conversation_id
    )

    for item in reversed(history):

        if item.get("role") == "user":

            return item.get(
                "message",
                ""
            )

    return ""


# =========================================================
# CLEAR CONVERSATION
# =========================================================

def clear_conversation(
    conversation_id: str
) -> None:

    if conversation_id in _conversations:

        del _conversations[
            conversation_id
        ]