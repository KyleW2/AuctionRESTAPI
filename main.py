from fastapi import FastAPI
from item import Item

app = FastAPI()

# Advanced database system
items = []

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/items/")
def post_item(item_name: str, starting_bid: float):
    temp = Item(len(items), item_name, starting_bid)
    items.append(temp)

    return temp.JSONResponse()

@app.get("/items/")
def read_items():
    out = {}
    
    for i in range(0, len(items)):
        out[i] = items[i].JSONResponse()
    
    return out

@app.get("/items/{item_id}")
def read_item_by_id(item_id: int):
    if item_id > len(items)-1 or item_id < 0:
        return {"message": "Index out of bounds"}
    
    return items[item_id].JSONResponse()
