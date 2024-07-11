import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from BotManager import BotManager
from databaseManager import dbManager
import logging
from privilegeManager import privilegeManager

privMen = privilegeManager.getInstance()

#logging.basicConfig(level=logging.INFO)  # Set the base logging level to INFO
#logger = logging.getLogger('discord')  # Get the logger for the 'discord' library
#logger.setLevel(logging.DEBUG) 

dbM = dbManager.getInstance()
load_dotenv()

bot = commands.Bot("DEMOCRACY!", intents=discord.Intents.default())

Token = os.getenv("DISCORD_BOT_TOKEN")

BotManager.setBot(bot)



import Commands.econ
import Commands.rat
import Commands.govern
import Commands.debug
import Commands.MichiMemory

from Routines import memory

import Events.onReady

bot.run(Token)