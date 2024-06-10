import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import get_db

test_db = []

def get_test_db():
    return test_db
#     try:
#         return test_db
#     finally:
#         test_db = []

@pytest.fixture(scope="function")
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

    global test_db
    test_db = []

# integration test
def test_read_todos_returns_correct_number_of_element(client):
    # given
    get_skip = 5
    get_limit = 10


    # Create 15 TODO
    for i in range(1, 16):
        print(i)
        new_todo = {
            "title": "Update User Profile",
            "description": "Change email address for user ID 123",
            "completed": False
        }

        result_todo = {
            "id": i,
            "title": "Update User Profile",
            "description": "Change email address for user ID 123",
            "completed": False
        }
        print(result_todo)

        response = client.post(
            "/todos/",
            json=new_todo,
        )

        print(response.json())
        assert response.status_code == 200
        assert response.json() == result_todo

    # https://apidog.com/articles/http-request-parameters-guide/
    # http://127.0.0.1:8000/todos/?skip=5&limit=10
    response = client.get(f"/todos?skip={get_skip}&limit={get_limit}")
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 10
    
# pytest tests/tests_main.py
