from fastapi import FastAPI
from item import Item
import idgen

app = FastAPI()

# Advanced database system
items = []

def getIndexFromID(id):
    for i in range(0, len(items)):
        if items[i].getID() == id:
            return i
    
    return -1

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/items/")
def post_item(item_name: str, starting_bid: float):
    temp = Item(idgen.genID(), item_name, starting_bid)
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
    if getIndexFromID(item_id) > -1:
        return items[getIndexFromID(item_id)].JSONResponse()

    return {"message": "Item not found"}

@app.delete("/items/{item_id}")
def del_item_by_id(item_id: int):
    if getIndexFromID(item_id) > -1:
        del items[getIndexFromID(item_id)]
        return {"deleted": item_id}
    
    return {"message": "Item not found"}
    
@app.put("/items/{item_id}")
def update_item_name(item_id: int, new_name: str):
    if getIndexFromID(item_id) > -1:
        if new_name != "":
            items[getIndexFromID(item_id)].setName(new_name)
            return items[getIndexFromID(item_id)].JSONResponse()
        return {"message": "Item name cannot be empty"}
    
    return {"message": "Item not found"}

@app.put("/items/{item_id}")
def place_bid(item_id: int, bid_amount: int):
    if getIndexFromID(item_id) > -1:
        bid_placed = items[getIndexFromID(item_id)].bid(bid_amount)

        if bid_placed:
            return items[getIndexFromID(item_id)].JSONResponse()
        return {"message": "Bid amount must be higher than current bid"}
    
    return {"message": "Item not found"}