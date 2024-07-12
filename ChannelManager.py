from BotManager import BotManager
class ChannelManager():
    ChannelManagers = {}
    
    @staticmethod
    def getInstance(guildID):
        if guildID not in ChannelManager.ChannelManagers:
            ChannelManager.ChannelManagers[guildID] = ChannelManager(guildID)
        return ChannelManager.ChannelManagers[guildID]
    
    def __init__(self, guildID ):
        self.StockChannel = 802655885008437268
        self.VoteChannel = 1260247977075671050
        self.LogChannel = 1242236502486810657
        self.ConstitutionChannel = 1259988043327340745
        
        self.guildID = guildID
        self.bot = BotManager.getBot()
        self.channels = {}
    

    async def sendOnStockChannel(self, message=None, embed=None, view=None):
        channel = self.bot.get_channel(self.StockChannel)
        await channel.send(message, embed=embed, view=view)
    
    async def sendOnVoteChannel(self, message=None, embed=None, view=None):
        channel = self.bot.get_channel(self.VoteChannel)
        await channel.send(message, embed=embed, view=view)
    
    async def sendOnLogChannel(self, message=None, embed=None, view=None):
        channel = self.bot.get_channel(self.LogChannel)
        await channel.send(message, embed=embed, view=view)
    
    async def sendOnConstitutionChannel(self, message=None, embed=None, view=None):
        channel = self.bot.get_channel(self.ConstitutionChannel)
        await channel.send(message, embed=embed, view=view)
    