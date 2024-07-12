import VoteSystem.VoteData as VoteData

class VoteManager:
    VoteManagers = {}

    @staticmethod
    def getVoteManager(guildID):
        if guildID not in VoteManager.VoteManagers:
            VoteManager.VoteManagers[guildID] = VoteManager(guildID)
        return VoteManager.VoteManagers[guildID]

    def __init__(self, guildID):
        self.guildID = guildID
        self.VoteQue = []

    def startVote(self, title, description, voteKind, present: list[int]):
        self.VoteQue.append(VoteData.Vote(title=title, description=description, voteKind=voteKind, present=present))
        return len(self.VoteQue) - 1
    
    def getVote(self, voteID):
        return self.VoteQue[voteID]

