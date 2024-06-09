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


# Report 2 Get request returns incorrect number of todos

## Description

1) Delete all todos

2) Create 15 todos

3) Send a GET request to `/todos` with `skip=5` and `limit=10`

## Expected result

Status `200 OK`

Received 10 Todos

## Actual result

Status `200 OK`

Received 5 Todos

# Report 3 Updating a todo returns null values

## Description

1) Create a todo

```json
{
  "title": "Update User Profile",
  "description": "Change email address for user ID 123",
  "completed": false
}
```

2) Get it by id GET `/todos/4`

3) Send a PATCH request  `/todos/4`
```json
{
  "title": "Finish Updating User Profile"
}
```

4) Get it by id GET `/todos/4` again

## Expected result

```json
{
  "title": "Finish Updating User Profile",
  "description": "Change email address for user ID 123",
  "completed": false
}
```

## Actual result 

Todo with null values

