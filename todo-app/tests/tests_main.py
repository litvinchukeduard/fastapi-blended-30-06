'''
Report 2 Get request returns incorrect number of todos
Description

    Delete all todos

    Create 15 todos

    Send a GET request to /todos with skip=5 and limit=10

Expected result

Status 200 OK

Received 10 Todos
Actual result

Status 200 OK

Received 5 Todos
'''

from fastapi.testclient import TestClient
from pytest import fixture

from app.main import app
from app.models import get_db, Todo

test_db = [
        Todo(id=1, title="Learn FastAPI", description="Study FastAPI framework", completed=False),
        Todo(id=2, title="Build API", description="Build an API with FastAPI", completed=False),
    ]

def get_test_db():
    return test_db

@fixture(scope="module")
def client():
    client = TestClient(app)
    app.dependency_overrides[get_db] = get_test_db
    return client

def test_create_todo_success(client):
    # given
    new_todo = {
        "title": "Report a bug",
        "description": "Create a bug report for /todos",
        "completed": True
    }
    # when
    response = client.post('/todos', json=new_todo)

    # then
    assert response.status_code == 200

def test_get_all_todos_correct_number(client):
    # given

    # Deleting all todos
    response = client.get('/todos/?skip=0&limit=10')
    for todo in response.json():
        client.delete(f"/todos/{todo['id']}")

    response = client.get('/todos/?skip=0&limit=10')
    assert len(response.json()) == 0

    # Create 20 todo
    new_todo = {
        "title": "Report a bug",
        "description": "Create a bug report for /todos",
        "completed": True
    }
    for _ in range(1, 21):
        client.post('/todos', json=new_todo)

    response = client.get('/todos/?skip=0&limit=20')
    assert len(response.json()) == 20

    # when
    response = client.get('/todos/?skip=5&limit=10')

    # then
    assert response.status_code == 200
    assert len(response.json()) == 10