import datetime

from discord.ext import tasks

from Backend.databaseManager import dbManager
from discordBackend.ChannelManager import ChannelManager
import discordBackend.EmbedGenerator as EmbedGenerator
import Economy.math as math
from discordBackend.BotManager import BotManager

dbM = dbManager.getInstance()

base = 6.52

halbesKilo = (base/53)*50

wertvon1kEUR = halbesKilo

bot = BotManager.getBot()

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
    if chance:
        val = dbM.get_company_value(company_id)
        new_val = val (val * chance)
        dbM.set_company_value(company_id, new_val)

    if math.random_bool(0.01):
        chance = -1
        return dbM.set_company_value(company_id, 0)
    return (chance, new_val)

def stockStuff():
    changeList = []
    companies = dbM.get_all_companies()
    for company in companies:
        old = dbM.get_company_value(company[0])
        stuff = applyStockChance(company[0])
        changeList.append({"name": dbM.get_company_name(company[0]), "change": round(stuff[0]*100, 2), "new": round(stuff[1], 2), "old": round(old, 2)})
    return changeList

@tasks.loop(minutes=1)
async def stockUpdate():
    now = datetime.datetime.now()
    if now.minute != 0:
        return
    changeList = stockStuff()
    embeds = await EmbedGenerator.generateStockChangeEmbed(changeList)
    for embed in embeds:
        await ChannelManager.getInstance(776823258385088552).sendOnStockChannel(embed=embed)

async def debuGStockUpdate():
    changeList = stockStuff()
    embeds = await EmbedGenerator.generateStockChangeEmbed(changeList)
    for embed in embeds:
        await ChannelManager.getInstance(776823258385088552).sendOnStockChannel(embed=embed)

def getWertinEUR(money):
    return round((money / 1000 * halbesKilo),2)