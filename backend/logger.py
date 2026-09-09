import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


# =========================================================
# LOG DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "data" / "logs"

LOG_FILE = LOG_DIR / "agent_interactions.jsonl"


# =========================================================
# CREATE LOG DIRECTORY
# =========================================================

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# LOG CUSTOMER INTERACTION
# =========================================================

def log_interaction(
    result: Dict[str, Any]
) -> None:
    """
    Store one customer-agent interaction
    as a JSON Lines record.
    """

    record = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "conversation_id": result.get(
            "conversation_id"
        ),

        "message": result.get(
            "message"
        ),

        "final_intent": result.get(
            "final_intent"
        ),

        "final_confidence": result.get(
            "final_confidence"
        ),

        "routing_method": result.get(
            "routing_method"
        ),

        "routing_action": result.get(
            "routing_action"
        ),

        "ml_intent": result.get(
            "ml_intent"
        ),

        "ml_confidence": result.get(
            "ml_confidence"
        ),

        "ai_used": result.get(
            "ai_used"
        ),

        "ai_intent": result.get(
            "ai_intent"
        ),

        "ai_confidence": result.get(
            "ai_confidence"
        ),

        "success": result.get(
            "success"
        ),

        "response": result.get(
            "response"
        ),

        "order_id": result.get(
            "order_id"
        ),

        "customer_name": result.get(
            "customer_name"
        ),

        "n8n": result.get(
            "n8n"
        ),
    }


    # =====================================================
    # WRITE JSONL RECORD
    # =====================================================

    with LOG_FILE.open(
        "a",
        encoding="utf-8",
    ) as file:

        file.write(
            json.dumps(
                record,
                ensure_ascii=False,
                default=str,
            )
            + "\n"
        )


# =========================================================
# READ LOGS
# =========================================================

def read_interactions():
    """
    Read all stored interactions.
    """

    if not LOG_FILE.exists():
        return []


    interactions = []


    with LOG_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue


            try:

                interactions.append(
                    json.loads(line)
                )

            except json.JSONDecodeError:

                continue


    return interactions