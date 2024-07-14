from discord.ext import tasks
import discord
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
        bot = BotManager.getBot()
        gl = bot.get_guild(776823258385088552)
        bro = gl.get_member(546434993690247191)
        if bro.status == discord.Status.offline or bro.status == discord.Status.idle or type(bro.status) == str:
            return
        Mid = dbM.get_random_memory()
        Mid = Mid[0]
        if Mid == None:
            return
        print(Mid)
        chan = bot.get_channel(random.choice(randooo))
        ques = dbM.get_question(Mid)
        print(ques)
        await chan.send("<@546434993690247191>", embed=await EmbedGenerator.generateMemoryQuestionEmbed(ques), view=Views.MemoryView(bot,Mid))
