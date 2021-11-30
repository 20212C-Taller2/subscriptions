from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

expected_subscriptions = [{"code": "BASIC", "description": "Basic Subscription", "price": 10.0, "course_limit": 5},
                          {"code": "FREE", "description": "Free Subscription", "price": 0.0, "course_limit": 3},
                          {"code": "FULL", "description": "Full Subscription", "price": 20.0, "course_limit": 7}]


def test_get_subscriptions():
    response = client.get("/subscriptions")
    assert response.status_code == 200
    assert response.json() == expected_subscriptions
