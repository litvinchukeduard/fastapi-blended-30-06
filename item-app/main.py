import uvicorn
from decimal import Decimal

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    quantity: int
    price: Decimal

class Inventory(BaseModel):
    items: List[Item] = []

inventory = Inventory()

def get_db():
    return inventory

@app.post("/add_item/")
def add_item(item: Item, db: Inventory = Depends(get_db)):
    print(db.items)
    for i in db.items:
        if i.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists.")
        if i.name == item.name:
            raise HTTPException(status_code=400, detail="Item with this name already exists.")
    db.items.append(item)
    return {"message": "Item added successfully", "item": item}

@app.get("/get_item/{item_id}")
def get_item(item_id: int, db: Inventory = Depends(get_db)):
    for item in db.items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/list_items/")
def list_items(min_quantity: Optional[int] = None, db: Inventory = Depends(get_db)):
    if min_quantity:
        filtered_items = [item for item in db.items if item.quantity >= min_quantity]
        return filtered_items
    return db.items

@app.put("/update_item/{item_id}")
def update_item(item_id: int, item: Item, db: Inventory = Depends(get_db)):
    for i, existing_item in enumerate(db.items):
        if existing_item.id == item_id:
            db.items[i] = item
            return {"message": "Item updated successfully", "item": item}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/delete_item/{item_id}")
def delete_item(item_id: int, db: Inventory = Depends(get_db)):
    for i, item in enumerate(db.items):
        if item.id == item_id:
            del db.items[i]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/total_value/")
def total_value(db: Inventory = Depends(get_db)):
    # total_sum = Decimal('0.0')
    # for item in db.items:
    #     total_sum += item.price * item.quantity
    # return {"total_value": total_sum}
    total = sum(item.price * item.quantity for item in db.items)
    return {"total_value": total}

# uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)