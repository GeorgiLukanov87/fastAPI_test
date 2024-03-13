from typing import Optional

from fastapi import FastAPI, Path

app = FastAPI()


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


@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description="The ID you want to see.", gt=0, lt=4)):
    return products[item_id]


@app.get("/get-by-name")
def get_item_by_name(*, name: Optional[str] = None):
    for item_id in products:
        if products[item_id]["name"] == name:
            return products[item_id]

    return {"Data": "Not found!"}

# http://127.0.0.1:8000/get-by-name?name=Milk = {"name":"Milk","price":2.39,"brand":"Nestle"}
# http://127.0.0.1:8000/get-by-name?name=Eggs = {"name":"Eggs","price":4.39,"brand":"Home"}
