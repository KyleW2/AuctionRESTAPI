import random

class IDGen():
    def __init__(self):
        self.id = self.genID()

    def genID(self):
        return random.randint(100000, 999999)
