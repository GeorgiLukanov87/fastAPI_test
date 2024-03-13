from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


products = {
    1: {
        "name": "Milk",
        "price": 2.39,
        "brand": "Nestle"
    },
    2: {
        "name": "Fanta",
        "price": 1.39,
        "brand": "Coca-Cola"
    },
    3: {
        "name": "Eggs",
        "price": 4.39,
        "brand": "Home"
    },
}
