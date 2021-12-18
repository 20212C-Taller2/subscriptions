import random
import string

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_retrieve_course():
    course_data = {
        "course_id": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)),
        "owner_id": "1",
        "subscription_code": "BASIC"
    }

    response = client.post("/courses/", json=course_data)
    assert response.status_code == 200
    assert response.json() == course_data

    response = client.get(f"/courses/{course_data['course_id']}", json=course_data)
    assert response.status_code == 200
    assert response.json() == course_data
