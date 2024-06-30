'''
# Report 1 Creating a new TODO returns status 500

## Description

Send a POST request to `/todos`

```json
{
  "title": "Report a bug",
  "description": "Create a bug report for /todos",
  "completed": true
}
```

## Expected result

Status `200 OK`

## Actual result 

Status `500 Internal Server Error`
'''

from fastapi.testclient import TestClient
from pytest import fixture

from app.main import app
from app.models import get_db

def get_test_db():
    test_db = []
    # global test_db
    try:
        yield test_db
    finally:
        test_db = []

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
