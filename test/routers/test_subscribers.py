def test_create_retrieve_subscriber(client):
    subscriber_id = "1"

    response = client.post("/subscribers/", json={"subscriber_id": subscriber_id})
    assert response.status_code == 200
    assert response.json()["subscriber_id"] == subscriber_id

    response = client.get(f"/subscribers/{subscriber_id}")
    assert response.status_code == 200
    assert response.json()["subscriber_id"] == subscriber_id
