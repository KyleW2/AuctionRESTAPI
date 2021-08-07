from fastapi import FastAPI
from item import Item

app = FastAPI()
items = []

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/items/")
def post_item(item_name: str, starting_bid: float):
    temp = Item(len(items), item_name, starting_bid)
    items.append(temp)

    return temp.JSONResponse()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id > len(items)-1 or item_id < 0:
        return {"message": "Index out of bounds"}
    
    return items[item_id].JSONResponse()