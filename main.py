from typing import Optional
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI()



class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None



class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None



@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


products = {
    1:
        {
            "name": "Milk",
            "price": 2.39,
            "brand": "Nestle"
        },
    2:
        {
            "name": "Bread",
            "price": 1.39,
            "brand": "HomeMade"
        },
    3:
        {
            "name": "Eggs",
            "price": 4.39,
            "brand": "Home"
        },
}

inventory = {}


@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description="The ID you want to see.", gt=0, lt=4)):
    if item_id not in inventory:
        return {"Error": "ID not found!"}
    return inventory[item_id]


@app.get("/get-by-name")
async def get_item_by_name(*, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]

    return {"Data": "Not found!"}

# http://127.0.0.1:8000/get-by-name?name=Milk = {"name":"Milk","price":2.39,"brand":"Nestle"}
@app.post("/create-item/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item ID already exist!"}

    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
async def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item ID does not exist!"}

    if item.name is not None:
        inventory[item_id] = item.name

    if item.price is not None:
        inventory[item_id] = item.price

    if item.brand is not None:
        inventory[item_id] = item.brand

    inventory[item_id].update(item)
    return inventory[item_id]


@app.delete("/delete-item")
async def delete_item(item_id: int = Query(..., description="ID of the item to delete,gt=0")):
    if item_id not in inventory:
        return {"Error": "ID does not exist!"}

    del inventory[item_id]
    return {"Succes": "Item deleted!"}


"""
From chat GPT

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

# Define a Pydantic model for our data
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

app = FastAPI()

# In-memory database
database: Dict[int, Item] = {}

# Counter for generating unique IDs
id_counter = 0

# Create operation
@app.post("/items/")
async def create_item(item: Item):
    global id_counter
    id_counter += 1
    database[id_counter] = item
    return {"id": id_counter, **item.dict()}

# Read operation
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = database.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update operation
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    database[item_id] = item
    return {"id": item_id, **item.dict()}

# Delete operation
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    del database[item_id]
    return {"message": "Item deleted"}
"""
