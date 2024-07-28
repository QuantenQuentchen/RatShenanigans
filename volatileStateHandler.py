

class VolatileStateHandler():

    Instance = None

    def getInstance():
        if VolatileStateHandler.Instance is None:
            VolatileStateHandler.Instance = VolatileStateHandler()
        return VolatileStateHandler.Instance
    
    def __init__(self):
        self.funny = False
        self.furry = False
        self.donAsk = False
        self.doMarket = True
        self.kevin = False

    def setKevin(self, state):
        self.kevin = state
    
    def getKevin(self):
        return self.kevin

    def setFurry(self, state):
        self.furry = state

    def getFurry(self):
        return self.furry

    def setFunny(self, state):
        self.funny = state
    
    def getFunny(self):
        return self.funny
    
    def setDonAsk(self, state):
        self.donAsk = state

    def getDonAsk(self):
        return self.donAsk
    
    def setDoMarket(self, state):
        self.doMarket = state
    
    def getDoMarket(self):
        return self.doMarket