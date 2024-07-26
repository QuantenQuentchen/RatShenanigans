from discordBackend.BotManager import BotManager
from Backend.prefManager import PrefManager
class ChannelManager():
    ChannelManagers = {}
    

    @staticmethod
    def getInstance(guildID):
        if guildID not in ChannelManager.ChannelManagers:
            ChannelManager.ChannelManagers[guildID] = ChannelManager(guildID)
        return ChannelManager.ChannelManagers[guildID]
    
    def __init__(self, guildID):
        self.prefMan = PrefManager.getInstance()
        #Hardcoded Channels
        self.StockChannel = self.prefMan.get_channel(PrefManager.kind.Stock, guildID, 1242236502486810657)
        self.VoteChannel = self.prefMan.get_channel(PrefManager.kind.Vote, guildID, 1260247977075671050)
        self.LogChannel = self.prefMan.get_channel(PrefManager.kind.Log, guildID, 1242236502486810657)
        self.ConstitutionChannel = self.prefMan.get_channel(PrefManager.kind.Constitution, guildID, 1259988043327340745)
        
        self.guildID = guildID
        self.bot = BotManager.getBot()
        self.channels = {}
    

    async def sendOnStockChannel(self, message=None, embed=None, view=None):
        #used to send a message defined by message, embed and views to specified Channel
        self.StockChannel = self.prefMan.get_channel(PrefManager.kind.Stock, self.guildID)
        print(self.StockChannel)
        channel = self.bot.get_channel(self.StockChannel)
        await channel.send(message, embed=embed, view=view)
    
    async def sendOnVoteChannel(self, message=None, embed=None, view=None):
        self.VoteChannel = self.prefMan.get_channel(PrefManager.kind.Vote, self.guildID)
        channel = self.bot.get_channel(self.VoteChannel)
        await channel.send(message, embed=embed, view=view)
    
    async def sendOnLogChannel(self, message=None, embed=None, view=None):
        self.LogChannel = self.prefMan.get_channel(PrefManager.kind.Log, self.guildID)
        print(self.LogChannel)
        channel = self.bot.get_channel(self.LogChannel)
        await channel.send(message, embed=embed, view=view)
    
    async def sendOnConstitutionChannel(self, message=None, embed=None, view=None):
        self.ConstitutionChannel = self.prefMan.get_channel(PrefManager.kind.Constitution, self.guildID)
        channel = self.bot.get_channel(self.ConstitutionChannel)
        await channel.send(message, embed=embed, view=view)