import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import get_db

def get_test_db():
    return []

@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    app.dependency_overrides[get_db] = get_test_db
    return client

def test_create_todo_success(client):
    # given
    new_todo = {
        "title": "Update User Profile",
        "description": "Change email address for user ID 123",
        "completed": False
    }

    result_todo = {
        "id": 1,
        "title": "Update User Profile",
        "description": "Change email address for user ID 123",
        "completed": False
    }

    # when # main.create_todo(new_todo, db)
    response = client.post(
        "/todos/",
        json=new_todo,
    )

    print(response.json())

    # then
    assert response.status_code == 200
    assert response.json() == result_todo
