from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert "AI Customer Support" in response.text
    assert "SupportAI" in response.text


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_human_agent_escalation():
    response = client.post(
        "/chat",
        json={
            "message": "I want to speak to a human agent",
            "customer_name": "Maria",
            "order_id": "10002",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["final_intent"] == "contact_human_agent"
    assert data["success"] is True
    assert data["data"]["escalated"] is True


def test_order_tracking():
    response = client.post(
        "/chat",
        json={
            "message": "Where is my order?",
            "order_id": "10002",
            "customer_name": "Maria",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["final_intent"] == "track_order"
    assert data["success"] is True


def test_payment_issue():
    response = client.post(
        "/chat",
        json={
            "message": "I have a payment problem",
            "order_id": "10004",
            "customer_name": "Emma",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["final_intent"] == "payment_issue"


def test_refund_request():
    response = client.post(
        "/chat",
        json={
            "message": "I want to request a refund",
            "order_id": "10001",
            "customer_name": "Alex",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["final_intent"] in [
        "get_refund",
        "check_refund_policy",
    ]

def test_multiturn_refund():
    from agent.flows.refund_flow import REFUNDS

    REFUNDS["10001"]["refund_status"] = "not_requested"

    conversation_id = "TEST-AUTO-REFUND"

    first = client.post(
        "/chat",
        json={
            "message": "I want a refund",
            "conversation_id": conversation_id,
            "customer_name": "Alex",
        },
    )

    assert first.status_code == 200
    assert first.json()["final_intent"] == "get_refund"
    assert first.json()["success"] is False

    second = client.post(
        "/chat",
        json={
            "message": "10001",
            "conversation_id": conversation_id,
            "customer_name": "Alex",
        },
    )

    assert second.status_code == 200
    data = second.json()

    assert data["final_intent"] == "get_refund"
    assert data["success"] is True
    assert data["order_id"] == "10001"


def test_multiturn_cancel_order():
    conversation_id = "TEST-AUTO-CANCEL"

    first = client.post(
        "/chat",
        json={
            "message": "I want to cancel my order",
            "conversation_id": conversation_id,
            "customer_name": "Emma",
        },
    )

    assert first.status_code == 200
    assert first.json()["final_intent"] == "cancel_order"
    assert first.json()["success"] is False

    second = client.post(
        "/chat",
        json={
            "message": "10004",
            "conversation_id": conversation_id,
            "customer_name": "Emma",
        },
    )

    assert second.status_code == 200
    data = second.json()

    assert data["final_intent"] == "cancel_order"
    assert data["success"] is True
    assert data["order_id"] == "10004"


def test_multiturn_change_order():
    conversation_id = "TEST-AUTO-CHANGE"

    first = client.post(
        "/chat",
        json={
            "message": "I want to change my order",
            "conversation_id": conversation_id,
            "customer_name": "John",
        },
    )

    assert first.status_code == 200
    assert first.json()["final_intent"] == "change_order"
    assert first.json()["success"] is False

    second = client.post(
        "/chat",
        json={
            "message": "10003",
            "conversation_id": conversation_id,
            "customer_name": "John",
        },
    )

    assert second.status_code == 200
    assert second.json()["final_intent"] == "change_order"
    assert second.json()["success"] is False
    assert second.json()["order_id"] == "10003"

    third = client.post(
        "/chat",
        json={
            "message": "Wireless Mouse",
            "conversation_id": conversation_id,
            "customer_name": "John",
        },
    )

    assert third.status_code == 200
    data = third.json()

    assert data["final_intent"] == "change_order"
    assert data["success"] is False
    assert data["order_id"] == "10003"
    assert "already delivered" in data["response"]
