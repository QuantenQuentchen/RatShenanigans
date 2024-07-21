

class VolatileStateHandler():

    Instance = None

    def getInstance():
        if VolatileStateHandler.Instance is None:
            VolatileStateHandler.Instance = VolatileStateHandler()
        return VolatileStateHandler.Instance
    
    def __init__(self):
        self.funny = False
        self.furry = False

    def setFurry(self, state):
        self.furry = state

    def getFurry(self):
        return self.furry

    def setFunny(self, state):
        self.funny = state
    
    def getFunny(self):
        return self.funny