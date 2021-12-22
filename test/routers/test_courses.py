from decimal import Decimal

from app import constants
from app.services import walletService


def test_create_retrieve_course(client, subscriber, basic_subscription):
    course_data = {
        "course_id": "course1",
        "owner_id": subscriber.subscriber_id,
        "subscription_code": basic_subscription.code
    }

    response = client.post("/courses/", json=course_data)
    assert response.status_code == 200
    assert response.json() == course_data

    response = client.get(f"/courses/{course_data['course_id']}", json=course_data)
    assert response.status_code == 200
    assert response.json() == course_data


def test_add_student_to_course(client, subscriber, basic_subscription):
    course_data = {
        "course_id": "course1",
        "owner_id": subscriber.subscriber_id,
        "subscription_code": basic_subscription.code
    }

    class OverrideWallet:
        def deposit(self, addr: str, priv_key: str, amount: Decimal):
            return constants.EthTxProcessResult.OK

        def get_balance(self, addr: str):
            return 0

    client.app.dependency_overrides[walletService.WalletService] = OverrideWallet

    response = client.post("/courses/", json=course_data)
    assert response.status_code == 200

    response = client.post(f"/courses/{course_data['course_id']}/subscribeStudent",
                           json={"subscriber_id": course_data["owner_id"]})
    assert response.status_code == 404  # No active basic_subscription

    response = client.post(f"/subscribers/{subscriber.subscriber_id}/subscription",
                           json={"subscription_code": basic_subscription.code})
    assert response.status_code == 200

    response = client.post(f"/courses/{course_data['course_id']}/subscribeStudent",
                           json={"subscriber_id": course_data["owner_id"]})
    assert response.status_code == 200
    response = client.delete(f"/courses/{course_data['course_id']}/subscribeStudent/{course_data['owner_id']}")
    assert response.status_code == 200
