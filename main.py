from fastapi import FastAPI
from item import Item

app = FastAPI()

# Advanced database system
items = []

def inBounds(x):
    if x > 0 and x < len(items)-1:
        return True
    return False

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
    if inBounds(item_id):
        return items[item_id].JSONResponse()

    return {"message": "Index out of bounds"}

@app.delete("/items/{item_id}")
def del_item_by_id(item_id: int):
    if inBounds(item_id):
        del items[item_id]
        return {"deleted": item_id}
    
    return {"message": "Index out of bounds"}
    
@app.put("/items/{item_id}")
def update_item_name(item_id: int, new_name: str):
    if inBounds(item_id):
        if new_name != "":
            items[item_id].setName(new_name)
            return items[item_id].JSONResponse()
        return {"message": "Item name cannot be empty"}
    
    return {"message": "Index out of bounds"}