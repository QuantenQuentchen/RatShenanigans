from discordBackend.privilegeManager import privilegeManager
from discordBackend.BotManager import BotManager
from volatileStateHandler import VolatileStateHandler
import random
from data.staticKevinData import KevinArray

bot = BotManager.getBot()
privMen = privilegeManager.getInstance()

volStateHan = VolatileStateHandler.getInstance()

@bot.event
async def on_message(message):
    if privMen.isMemoryGuy(message.author) and volStateHan.getFunny():
        await message.reply(r"https://tenor.com/view/pegging-meme-sexiest-woman-alive2022-sonic-the-hedgehog-morbius-sweep-gif-25813254")
    if privMen.isFurry(message.author) and volStateHan.getFurry():
        await message.reply(r"https://tenor.com/view/furry-tf2-stfu-sussy-gif-21878916")
    if privMen.isSchewaun(message.author) and volStateHan.getDonAsk():
        await message.reply(r"https://tenor.com/view/speech-bubble-gif-27609617")
    if privMen.isKevin(message.author) and volStateHan.getKevin():
        await message.reply(random.choice(KevinArray))
