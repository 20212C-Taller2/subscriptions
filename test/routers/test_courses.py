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
