from BotManager import BotManager
from Routines.memory import randoPush
from Economy.manage import stockUpdate

bot = BotManager.getBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    randoPush.start()
    stockUpdate.start()