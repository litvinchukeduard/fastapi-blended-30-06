# Report 1 Can create duplicate items

## Description

1) Send a POST request to `/add_item`

```json
{
  "id": 2,
  "name": "Pen",
  "quantity": 0,
  "price": 0
}
```

2) Send another POST request tp `/add_item`

```json
{
  "id": 3,
  "name": "Pen",
  "quantity": 2,
  "price": 3
}
```

## Expected result

Status `400 Bad Request`

## Actual result 

Status `200 OK`


# Report 2 Can change the id of an item

## Description

1) Create an item by sending a POST request to `/add_item`

```json
{
  "id": 4,
  "name": "Paper",
  "quantity": 10,
  "price": 1
}
```

2) Update item, by sending PUT request tp `/update_item/4`

```json
{
  "id": 5,
  "name": "Paper",
  "quantity": 1,
  "price": 2
}
```

## Expected result

Status `400 Bad Request`

## Actual result

Status `200 OK`

# Report 3 Total price is calculated incorrectly

## Description

1) Delete all items

2) Create two items

```json
{
  "id": 4,
  "name": "Paper",
  "quantity": 1,
  "price": 0.1
}
```

```json
{
  "id": 5,
  "name": "Pen",
  "quantity": 1,
  "price": 0.2
}
```

3) Send request to calculate total value

## Expected result

```json
{
  "total_value": 0.3
}
```

## Actual result 

```json
{
  "total_value": 0.30000000000000004
}
```

