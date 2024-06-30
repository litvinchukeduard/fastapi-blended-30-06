'''
Report 3 Total price is calculated incorrectly
Description

    Delete all items

    Create two items

{
  "id": 4,
  "name": "Paper",
  "quantity": 1,
  "price": 0.1
}

{
  "id": 5,
  "name": "Pen",
  "quantity": 1,
  "price": 0.2
}

    Send request to calculate total value

Expected result

{
  "total_value": 0.3
}

Actual result

{
  "total_value": 0.30000000000000004
}
'''

from fastapi.testclient import TestClient
from pytest import fixture

from main import app
from main import Inventory, get_db


@fixture(scope="function")
def client():
    test_db = Inventory()
    def get_test_db():
        return test_db

    client = TestClient(app)
    app.dependency_overrides[get_db] = get_test_db
    return client

def test_create_item_duplicate_id_fail(client):
    # given
    new_item_one = {
        "id": 2,
        "name": "Pencil",
        "quantity": 0,
        "price": 0
    }
    new_item_two = {
        "id": 2,
        "name": "Pen",
        "quantity": 2,
        "price": 3
    }

    # when
    client.post('/add_item', json=new_item_one)
    response = client.post('/add_item', json=new_item_two)

    # then
    assert response.status_code == 400

def test_create_item_duplicate_name_fail(client):
    # given
    new_item_one = {
        "id": 2,
        "name": "Pen",
        "quantity": 0,
        "price": 0
    }
    new_item_two = {
        "id": 3,
        "name": "Pen",
        "quantity": 2,
        "price": 3
    }

    # when
    client.post('/add_item', json=new_item_one)
    response = client.post('/add_item', json=new_item_two)

    # then
    print(response.json())
    assert response.status_code == 400

def test_get_all_todos_correct_number(client):
    # given

    # Deleting all items
    response = client.get('/list_items')
    for item in response.json():
        client.delete(f"/delete_item/{item['id']}")

    # Create 2 items
    items = [
        {
            "id": 5,
            "name": "Pen",
            "quantity": 1,
            "price": 0.2
        },
        {
            "id": 6,
            "name": "Pencil",
            "quantity": 3,
            "price": 0.2
        }
    ]
    for i in range(len(items)):
        client.post('/add_item', json=items[i])

    # when
    response = client.get('/total_value')

    # then
    assert response.status_code == 200
    assert response.json()['total_value'] == 0.8