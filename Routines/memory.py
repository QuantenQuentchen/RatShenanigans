from discord.ext import tasks
from discordBackend.BotManager import BotManager
import datetime
import random
from Economy.math import random_bool
import discordBackend.EmbedGenerator as EmbedGenerator
import discordBackend.Views as Views
from Backend.databaseManager import dbManager

randooo = [802655885008437268, 824262527982632971, 834076218261372939, 1204276957886287892, 776823258967834676, 802618285580615731]
bot = BotManager.getBot()

dbM = dbManager.getInstance()

@tasks.loop(minutes=3)
async def randoPush():
    if random_bool(13.25):

        Mid = dbM.get_random_memory()
        if Mid == None:
            return
        chan = await bot.get_channel(random.choice(randooo))
        await chan.send("<@&546434993690247191>", embed=await EmbedGenerator.generateMemoryQuestionEmbed(dbM.get_question(Mid)), view=Views.MemoryView(bot,Mid))
