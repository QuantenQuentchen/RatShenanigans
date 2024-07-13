import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from discordBackend.BotManager import BotManager
from Backend.databaseManager import dbManager
import logging
from discordBackend.privilegeManager import privilegeManager

#Get's the privilege manager singelton instance
privMen = privilegeManager.getInstance()

#Debug Logger for pycord internals, commented out for now
#logging.basicConfig(level=logging.INFO)  # Set the base logging level to INFO
#logger = logging.getLogger('discord')  # Get the logger for the 'discord' library
#logger.setLevel(logging.DEBUG) 

#Get's the database manager singelton instance
dbM = dbManager.getInstance()
load_dotenv()

#Create the bot instance
bot = commands.Bot("DEMOCRACY!", intents=discord.Intents.default())

#Get the token from the environment
Token = os.getenv("DISCORD_BOT_TOKEN")

#Set the bot instance in the BotManager
BotManager.setBot(bot)


#Loads subcommands
#Commands are added via function decorators
#All Discord interaction needs to be async as the library is async i.e async def and await
import Commands.econ
import Commands.rat
import Commands.govern
import Commands.debug
import Commands.MichiMemory

from Routines import memory

import Events.onReady

bot.run(Token)