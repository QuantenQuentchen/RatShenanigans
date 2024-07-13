from discordBackend.BotManager import BotManager
from Routines.memory import randoPush
from Economy.manage import stockUpdate

bot = BotManager.getBot()

#Defines an Event that is called when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    randoPush.start()
    stockUpdate.start()