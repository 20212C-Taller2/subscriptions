from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

expected_subscriptions = [
    {
        "code": "FREE",
        "description": "Free Subscription"
    },
    {
        "code": "BASIC",
        "description": "Basic Subscription"
    },
    {
        "code": "FULL",
        "description": "Full Subscription"
    }
]


def test_get_subscriptions():
    response = client.get("/subscriptions")
    assert response.status_code == 200
    assert response.json() == expected_subscriptions
