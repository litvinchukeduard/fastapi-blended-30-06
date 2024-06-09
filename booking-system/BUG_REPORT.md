# Report 1 Can create users with duplicate emails

## Description

1) Create user

```json
{ "id": 1, "name": "John Doe", "email": "john@example.com" }
```

2) Create a second user with same email

```json
{ "id": 2, "name": "Jane Doe", "email": "john@example.com" }
```

## Expected result

Status `400 Bad Request`

## Actual result 

Status `200 OK`

# Report 2 Can book overlapping sessions

## Description

1) Create two sessions

```json
{ "id": 1, "title": "Session 1", "start_time": "2024-06-10T10:00:00", "end_time": "2024-06-10T11:00:00", "max_participants": 10 }
```

```json
{ "id": 2, "title": "Session 2", "start_time": "2024-06-10T11:00:00", "end_time": "2024-06-10T12:00:00", "max_participants": 10 }
```

2) Create a participant

```json
{ "id": 1, "name": "John Doe", "email": "john@example.com" }
```

3) Book session 1

4) Book session 2

## Expected result

Status `400 Bad Request`

## Actual result 

Status `200 OK`