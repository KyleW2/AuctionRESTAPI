from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from item import Item
import idgen

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Modern opensource lightweight dependency-free database
#
#        |
#        V
items = []

def getIndexFromID(id):
    for i in range(0, len(items)):
        if items[i].getID() == id:
            return i
    
    return -1

def HTMLItemResponse(request, index):
    return templates.TemplateResponse("item.html", {"request": request,
                                                        "item_name": items[index].getName(), 
                                                        "starting_bid": items[index].getStartingBid(),
                                                        "current_bid": items[index].getBid()
    })

def HTMLNotFoundResponse(request, message):
    return templates.TemplateResponse("item_not_found.html", {"request": request, "message": message})

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

@app.get("/items/{item_id}", response_class=HTMLResponse)
def read_item_by_id(request: Request, item_id: int):
    if getIndexFromID(item_id) > -1:
        #return items[getIndexFromID(item_id)].JSONResponse()
        return HTMLItemResponse(request, getIndexFromID(item_id))

    return HTMLNotFoundResponse(request, "")

@app.delete("/items/{item_id}", response_class=HTMLResponse)
def delete_item_by_id(request: Request, item_id: int):
    if getIndexFromID(item_id) > -1:
        del items[getIndexFromID(item_id)]
        return templates.TemplateResponse("item_deleted.html", {"request": request})
    
    return HTMLNotFoundResponse(request, "The item was not deleted")

@app.put("/items/{item_id}", response_class=HTMLResponse)
def update_item_name(request: Request, item_id: int, new_name: str):
    if getIndexFromID(item_id) > -1:
        if new_name != "":
            items[getIndexFromID(item_id)].setName(new_name)
            return HTMLItemResponse(request, getIndexFromID(item_id))
        return {"message": "Item name cannot be empty"}
    
    return HTMLNotFoundResponse(request, "")

@app.post("/items/{item_id}", response_class=HTMLResponse)
def post_bid(request: Request, item_id: int, bid_amount: int):
    if getIndexFromID(item_id) > -1:
        bid_placed = items[getIndexFromID(item_id)].bid(bid_amount)

        if bid_placed:
            return HTMLItemResponse(request, getIndexFromID(item_id))
        return {"message": "Bid amount must be higher than current bid"}
    
    return HTMLNotFoundResponse(request, "")