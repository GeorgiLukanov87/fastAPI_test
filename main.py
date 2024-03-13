from typing import Optional
from fastapi import FastAPI, Path
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
            "brand": "Nestle",
        },

    2:
        {
            "name": "Bread",
            "price": 1.39,
            "brand": "HomeMade",
        },

    3:
        {
            "name": "Eggs",
            "price": 4.39,
            "brand": "Home",
        },
}

inventory = {}


@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description="The ID you want to see.", gt=0, lt=4)):
    return inventory[item_id]


@app.get("/get-by-name")
async def get_item_by_name(*, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]

    return {"Data": "Not found!"}


# http://127.0.0.1:8000/get-by-name?name=Milk = {"name":"Milk","price":2.39,"brand":"Nestle"}
# http://127.0.0.1:8000/get-by-name?name=Eggs = {"name":"Eggs","price":4.39,"brand":"Home"}


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
