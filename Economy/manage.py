import datetime

from discord.ext import tasks

from Backend.databaseManager import dbManager
from discordBackend.ChannelManager import ChannelManager
import discordBackend.EmbedGenerator as EmbedGenerator
import Economy.math as math
from discordBackend.BotManager import BotManager
from volatileStateHandler import VolatileStateHandler

dbM = dbManager.getInstance()

#Fixwert für 0.53kg Knete in EUR
base = 6.52

#Dreisatz
halbesKilo = (base/53)*50

wertvon1kEUR = halbesKilo

bot = BotManager.getBot()


#Helper Functions for db-econ interactions
def remove_balance(discord_id, amount):
    current_balance = dbM.get_user_balance(discord_id)
    new_balance = current_balance - amount
    dbM.set_user_balance(discord_id, new_balance)

def add_balance(discord_id, amount):
    current_balance = dbM.get_user_balance(discord_id)
    new_balance = current_balance + amount
    dbM.set_user_balance(discord_id, new_balance)

def get_balance(discord_id):
    return dbM.get_user_balance(discord_id)

def transfer_balance(sender_id, receiver_id, amount):
    remove_balance(sender_id, amount)
    add_balance(receiver_id, amount)

def applyStockChance(company_id):
    chance = math.genStockChance()
    if math.random_bool(0.01):
        chance = -1
        dbM.set_company_value(company_id, 0)
    else:
        val = dbM.get_company_value(company_id)
        new_val = val + (val * chance)
        dbM.set_company_value(company_id, new_val)

    return (chance, new_val)


#Generalized outsourced random Stock modifications
def stockStuff():
    changeList = []
    companies = dbM.get_all_companies()
    for company in companies:
        old = dbM.get_company_value(company[0])
        stuff = applyStockChance(company[0])
        changeList.append({"name": dbM.get_company_name(company[0]), "change": round(stuff[0]*100, 2), "new": round(stuff[1], 2), "old": round(old, 2)})
    return changeList


#Task looped every minute
@tasks.loop(minutes=1)
async def stockUpdate():
    #following checks if the current minute is 0, if not the function returns, i.e that it runs only on the full hour
    now = datetime.datetime.now()
    if not VolatileStateHandler.getInstance().getDoMarket():
        return
    if now.minute != 0:
        return
    changeList = stockStuff()
    embeds = await EmbedGenerator.generateStockChangeEmbed(changeList)
    for embed in embeds:
        await ChannelManager.getInstance(776823258385088552).sendOnStockChannel(embed=embed)

#Same only as debug without checks, for yk debug
async def debuGStockUpdate():
    changeList = stockStuff()
    embeds = await EmbedGenerator.generateStockChangeEmbed(changeList)
    for embed in embeds:
        await ChannelManager.getInstance(776823258385088552).sendOnStockChannel(embed=embed)


#Idiotic helper function to convert to EUR
def getWertinEUR(money):
    #round is uesed to round to 2 decimal places, to not display full float precision
    return round((money / 1000 * halbesKilo),2)