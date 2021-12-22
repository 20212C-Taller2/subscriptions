from decimal import Decimal

from app import constants
from app.services import walletService


def test_create_retrieve_subscriber(client):
    subscriber_id = "1"

    response = client.post("/subscribers/", json={"subscriber_id": subscriber_id})
    assert response.status_code == 200
    assert response.json()["subscriber_id"] == subscriber_id

    response = client.get(f"/subscribers/{subscriber_id}")
    assert response.status_code == 200
    assert response.json()["subscriber_id"] == subscriber_id


def test_add_subscription(client, subscriber, basic_subscription):
    class OverrideWallet:
        def deposit(self, addr: str, priv_key: str, amount: Decimal):
            return constants.EthTxProcessResult.OK

        def get_balance(self, addr: str):
            return 0

    client.app.dependency_overrides[walletService.WalletService] = OverrideWallet
    response = client.post(f"/subscribers/{subscriber.subscriber_id}/subscription",
                           json={"subscription_code": basic_subscription.code})
    assert response.status_code == 200
