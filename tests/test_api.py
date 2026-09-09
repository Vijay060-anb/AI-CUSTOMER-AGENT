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