from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI(
    title="QuickStock",
    description="QuickStock is a lightweight and efficient API for managing inventory. Easily add, update, view, and delete items with built-in FastAPI performance and documentation. Perfect for developers needing a simple yet powerful backend solution.",
    version="1.0.0",
)


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    in_stock: bool = True


database: List[Item] = []


@app.get("/")
def read_root():
    return {"message": "Welcome to the Example API!"}


@app.get("/items", response_model=List[Item])
def get_items():
    """
    Get all items.
    """
    return database


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """
    Get a single item by its ID.
    """
    item = next((item for item in database if item.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    """
    Create a new item.
    """
    if any(existing_item.id == item.id for existing_item in database):
        raise HTTPException(status_code=400, detail="Item ID already exists")
    database.append(item)
    return item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    """
    Update an item by its ID.
    """
    for index, existing_item in enumerate(database):
        if existing_item.id == item_id:
            database[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    """
    Delete an item by its ID.
    """
    global database
    database = [item for item in database if item.id != item_id]
    return None
