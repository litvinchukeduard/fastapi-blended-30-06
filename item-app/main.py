from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    quantity: int
    price: float

class Inventory(BaseModel):
    items: List[Item] = []

inventory = Inventory()

@app.post("/add_item/")
def add_item(item: Item):
    for i in inventory.items:
        if i.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists.")
        if i.name == item.name:
            raise HTTPException(status_code=400, detail="Item with this name already exists.")
    inventory.items.append(item)
    return {"message": "Item added successfully", "item": item}

@app.get("/get_item/{item_id}")
def get_item(item_id: int):
    for item in inventory.items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/list_items/")
def list_items(min_quantity: Optional[int] = None):
    if min_quantity:
        filtered_items = [item for item in inventory.items if item.quantity >= min_quantity]
        return filtered_items
    return inventory.items

@app.put("/update_item/{item_id}")
def update_item(item_id: int, item: Item):
    for i, existing_item in enumerate(inventory.items):
        if existing_item.id == item_id:
            inventory.items[i] = item
            return {"message": "Item updated successfully", "item": item}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/delete_item/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(inventory.items):
        if item.id == item_id:
            del inventory.items[i]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/total_value/")
def total_value():
    total = sum(item.price * item.quantity for item in inventory.items)
    return {"total_value": total}

# uvicorn main:app --reload