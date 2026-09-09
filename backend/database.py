import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from supabase import create_client, Client


# Load environment variables from the project root .env file
load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing from .env")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is missing from .env")


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


def get_order(order_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve an order from the Supabase orders table.
    """

    if not order_id:
        return None

    response = (
        supabase
        .table("orders")
        .select("*")
        .eq("order_id", order_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def update_order(
    order_id: str,
    updates: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Update an existing order in Supabase.
    """

    if not order_id:
        return None

    response = (
        supabase
        .table("orders")
        .update(updates)
        .eq("order_id", order_id)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def create_order(order: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Create a new order in Supabase.
    """

    response = (
        supabase
        .table("orders")
        .insert(order)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def delete_order(order_id: str) -> bool:
    """
    Delete an order from Supabase.
    """

    if not order_id:
        return False

    response = (
        supabase
        .table("orders")
        .delete()
        .eq("order_id", order_id)
        .execute()
    )

    return bool(response.data)