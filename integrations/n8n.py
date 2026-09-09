import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()


N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


def send_to_n8n(
    agent_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Send the customer-agent result to n8n.
    """

    if not N8N_WEBHOOK_URL:
        return {
            "success": False,
            "message": "N8N_WEBHOOK_URL is not configured."
        }

    payload = {
        "message": agent_result.get("message"),
        "final_intent": agent_result.get("final_intent"),
        "final_confidence": agent_result.get("final_confidence"),
        "routing_method": agent_result.get("routing_method"),
        "ai_used": agent_result.get("ai_used"),
        "success": agent_result.get("success"),
        "response": agent_result.get("response"),
        "data": agent_result.get("data"),
    }

    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=10,
        )

        return {
            "success": response.ok,
            "status_code": response.status_code,
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "message": str(error),
        }