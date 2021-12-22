import pytest

from app.db.models import Subscription
from test.conftest import TestingSessionLocal

expected_subscriptions = [{"code": "BASIC", "description": "Basic Subscription", "price": 1e-06, "course_limit": 5},
                          {"code": "FREE", "description": "Free Subscription", "price": 0.0, "course_limit": 3},
                          {"code": "FULL", "description": "Full Subscription", "price": 1e-05, "course_limit": 10}]


@pytest.fixture
def client_with_subscriptions(client):
    db = TestingSessionLocal()
    for es in expected_subscriptions:
        s = Subscription(code=es["code"],
                         description=es["description"],
                         price=es["price"],
                         course_limit=es["course_limit"])
        db.add(s)
    db.commit()
    db.close()
    return client


def test_get_subscriptions(client_with_subscriptions):
    response = client_with_subscriptions.get("/subscriptions")
    assert response.status_code == 200
    assert response.json() == expected_subscriptions
