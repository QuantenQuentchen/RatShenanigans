class Vote:
    def __init__(self, title, description, voteKind, present: list[int], private: bool = False):
        self.title = title
        self.description = description
        self.voteKind = voteKind
        self.present = present
        self.private = private
        self.pro = set()
        self.abstain = set()
        self.con = set()
    
    def getPro(self) -> set[int]:
        return self.pro

    def addPro(self, voteeId):
        self.removeVotee(voteeId)
        self.pro.add(voteeId)

    def removePro(self, voteeId):
        self.pro.discard(voteeId)

    def getProNum(self) -> int:
        return len(self.pro)

    def getAbstain(self) -> set[int]:
            return self.abstain

    def addAbstain(self, voteeId):
        self.removeVotee(voteeId)
        self.abstain.add(voteeId)

    def removeAbstain(self, voteeId):
        self.abstain.discard(voteeId)

    def getAbstainNum(self) -> int:
        return len(self.abstain)

    def getCon(self) -> set[int]:
        return self.con

    def addCon(self, voteeId):
        self.removeVotee(voteeId)
        self.con.add(voteeId)

    def removeCon(self, voteeId):
        self.con.discard(voteeId)

    def getConNum(self) -> int:
        return len(self.con)

    def getPresentNum(self) -> int:
        return self.getAbstainNum() + self.getProNum() + self.getConNum()

    def removeVotee(self, voteeId):
        self.removePro(voteeId)
        self.removeAbstain(voteeId)
        self.removeCon(voteeId)
        
    def needRevote(self):
        return self.getProNum() == self.getConNum()

    def checkInValidity(self):
        if self.getPresentNum() >= 5:#self.getProNum() + self.getConNum() + self.getAbstainNum() == self.getPresentNum() and self.getPresentNum() >= 5:
            return False
        return True

    def checkSimpleMajority(self):
        return self.getProNum() > self.getConNum()
    
    def checkQualifiedMajority(self):
        return self.getProNum() > (self.getPresentNum()/3)*2 and self.checkSimpleMajority()

    def evaluate(self)-> bool:
        if self.checkInValidity():
            return -1
        if self.needRevote():
            return 0
        match self.voteKind:
            case 0:
                return self.checkSimpleMajority()
            case 1:
                return self.checkQualifiedMajority()
            case _:
                return False