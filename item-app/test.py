import pytest
from fastapi.testclient import TestClient

from main import app

@pytest.fixture(scope="function")
def client():
    client = TestClient(app)
    return client

def test_add_item_duplicate(client):
    # given
    item_one_request = {
        "id": 2,
        "name": "Pen",
        "quantity": 0,
        "price": 0
    }

    item_two_request = {
        "id": 3,
        "name": "Pen",
        "quantity": 2,
        "price": 3
    }

    # response = client.post(
    #     "/add_item/",
    #     json=item_one_request,
    # )
    client.post(
        "/add_item/",
        json=item_one_request,
    )

    # assert response.status_code == 200

    response = client.post(
        "/add_item/",
        json=item_two_request,
    )

    assert response.status_code == 400