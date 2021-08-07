class Item():
    def __init__(self, id, name, startingBid):
        self.id = id
        self.name = name
        self.startingBid = startingBid
        self.currentBid = startingBid
    
    def getID(self):
        return self.id
    def getName(self):
        return self.name
    def getStartingBid(self):
        return self.startingBid
    def getBid(self):
        return self.currentBid
    
    def setName(self, name):
        self.name = name
    def setStartingBid(self, startingBid):
        self.startingBid = startingBid
    
    def bid(self, bid):
        if bid > self.currentBid:
            self.currentBid = bid
            return True
        return False
    
    def JSONResponse(self):
        return {"item_id": self.id, "item_name": self.name, "current_bid": self.currentBid}