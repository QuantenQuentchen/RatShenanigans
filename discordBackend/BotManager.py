class BotManager():
    bot = None
    #Used to retrieve the bot instance over the entire project
    def setBot(bot):
        BotManager.bot = bot
    
    def getBot():
        return BotManager.bot