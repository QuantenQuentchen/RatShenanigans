import discord
from discord.ext import commands, tasks
import sqlite3
from dotenv import load_dotenv
import os
import random
import datetime
import math

import Views
import VoteManager
import EmbedGenerator as EmbedGenerator

base = 6.52

halbesKilo = (base/53)*50

wertvon1kEUR = halbesKilo

StockChannel = 802655885008437268

load_dotenv()

connection = sqlite3.connect("democracy.db")
cur = connection.cursor()

constitu = []

chanceArr = []

for i in range(70):
    chanceArr.append(-1)

for i in range(25):
    chanceArr.append(0)

for i in range(4):
    chanceArr.append([1.1, 3.0])

chanceArr.append(4)

def random_bool(true_percentage):
    return random.random() < true_percentage / 100.0

def genStockChance():
    return random.uniform(-0.9, 3.0)

def get_all_companies():
    cur.execute("SELECT company_id FROM companies")
    result = cur.fetchall()

    return result

def set_company_value(company_id, value):
    cur.execute("UPDATE companies SET value = ? WHERE company_id = ?", (value, company_id))
    connection.commit()

def get_company_value(company_id):
    cur.execute("SELECT value FROM companies WHERE company_id = ?", (company_id,))
    result = cur.fetchone()

    return result[0] if result else None

def get_company_name(company_id):
    cur.execute("SELECT name FROM companies WHERE company_id = ?", (company_id,))
    result = cur.fetchone()

    return result[0] if result else None

def round_up(value, digits):
    scale = 10 ** digits
    return math.ceil(value * scale) / scale

def getChance():
    choice = random.choice(chanceArr)
    if type(choice) == int:
        return choice
    else:
        return random.uniform(choice[0], choice[1])
    
def calcChance(chance, input):
    res = chance
    result = round_up(input*res, 2)
    if res == -1:
        result = 0
    if res == 0:
        result = input
    return result

def parseTxt(txt):
    currentArticel = {}
    currentParagraph = {"title": "", "content": ""}
    for line in txt:
        if len(line) == 0:
            continue
        if line.startswith("Artikel"):
            line = line.replace("\n", "")
            line = line.replace("\t", "")
            if(len(currentArticel) != 0):
                constitu.append(currentArticel)
            if(currentParagraph["title"] != "" and currentParagraph["content"] != ""):
                currentArticel["paragraphs"].append(currentParagraph)
            currentArticel = {"title": line, "paragraphs": []}
            currentParagraph = {"title": "", "content": ""}
        elif line.startswith("\t-"):
            line = line.replace("\n", "")
            line = line.replace("\t", "")
            currentArticel["paragraphs"].append(currentParagraph)
            currentParagraph = {"title": "", "content": ""}
            currentParagraph["title"] = line
        elif line.startswith("\t\t"):
            line = line.replace("\n", "")
            line = line.replace("\t", "")
            currentParagraph["content"] += line + "\n"
    for i in constitu:
        i["paragraphs"] = [paragraph for paragraph in i["paragraphs"] if not (paragraph.get("title") == "" and paragraph.get("content") == "")]


def create_tables():
    connection = sqlite3.connect("democracy.db")
    cur = connection.cursor()

    # Create the users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            discord_id INTEGER PRIMARY KEY,
            balance REAL
        );
    """)

    # Create the companies table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value REAL NOT NULL
        );
    """)

    # Create the user_stocks table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_stocks (
            discord_id INTEGER,
            company_id INTEGER,
            stocks_held INTEGER,
            PRIMARY KEY (discord_id, company_id),
            FOREIGN KEY (discord_id) REFERENCES users(discord_id),
            FOREIGN KEY (company_id) REFERENCES companies(company_id)
        );
    """)

    connection.commit()

def drop_tables():
    connection = sqlite3.connect("democracy.db")
    cur = connection.cursor()

    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("DROP TABLE IF EXISTS companies")
    cur.execute("DROP TABLE IF EXISTS user_stocks")
    cur.execute("DROP TABLE IF EXISTS constitution_changes")

    connection.commit()

create_tables()

def does_user_exist(discord_id):
    cur.execute("SELECT 1 FROM users WHERE discord_id = ?", (discord_id,))
    result = cur.fetchone()

    return True if result else False

def get_user_balance(discord_id):

    add_user(discord_id, 100)

    cur.execute("SELECT balance FROM users WHERE discord_id = ?", (discord_id,))
    result = cur.fetchone()


    return result[0]

def set_user_balance(discord_id, new_balance):

    add_user(discord_id, 100)

    cur.execute("UPDATE users SET balance = ? WHERE discord_id = ?", (new_balance, discord_id))
    connection.commit()

def get_company_value(company_id):
    
        cur.execute("SELECT value FROM companies WHERE company_id = ?", (company_id,))
        result = cur.fetchone()
    
    
        return result[0] if result else None

def get_user_stocks(discord_id, company_id):

    cur.execute("SELECT stocks_held FROM user_stocks WHERE discord_id = ? AND company_id = ?", (discord_id, company_id))
    result = cur.fetchone()

    return result[0] if result else None

def get_all_user_stocks(discord_id):
    
        cur.execute("SELECT company_id, stocks_held FROM user_stocks WHERE discord_id = ?", (discord_id,))
        result = cur.fetchall()
    
    
        return result

def add_user(discord_id, balance):
    if not does_user_exist(discord_id):
        cur.execute("INSERT INTO users (discord_id, balance) VALUES (?, ?)", (discord_id, balance))
        connection.commit()

def add_company(name, value):
    cur.execute("SELECT 1 FROM companies WHERE name = ?", (name,))
    result = cur.fetchone()
    if result:
        return
    cur.execute("INSERT INTO companies (name, value) VALUES (?, ?)", (name, value))
    connection.commit()

def add_stocks_to_user(discord_id, company_id, additional_stocks):
    # Check if the user already has stocks of the company
    cur.execute("SELECT stocks_held FROM user_stocks WHERE discord_id = ? AND company_id = ?", (discord_id, company_id))
    result = cur.fetchone()

    if result:
        # User already has stocks, update the amount
        current_stocks = result[0]
        new_total = current_stocks + additional_stocks
        cur.execute("UPDATE user_stocks SET stocks_held = ? WHERE discord_id = ? AND company_id = ?", (new_total, discord_id, company_id))
    else:
        # User does not have stocks of this company, insert a new record
        cur.execute("INSERT INTO user_stocks (discord_id, company_id, stocks_held) VALUES (?, ?, ?)", (discord_id, company_id, additional_stocks))
    
    connection.commit()

def increment_company_value(company_id, percentage):
        current_value = get_company_value(company_id)
        increment = current_value*percentage
        cur.execute("UPDATE companies SET value = value + ? WHERE company_id = ?", (increment, company_id))
        connection.commit()

def remove_balance(discord_id, amount):
    current_balance = get_user_balance(discord_id)
    new_balance = current_balance - amount
    set_user_balance(discord_id, new_balance)

def add_balance(discord_id, amount):
    current_balance = get_user_balance(discord_id)
    new_balance = current_balance + amount
    set_user_balance(discord_id, new_balance)

def get_balance(discord_id):
    return get_user_balance(discord_id)

def transfer_balance(sender_id, receiver_id, amount):
    remove_balance(sender_id, amount)
    add_balance(receiver_id, amount)

bot = commands.Bot("DEMOCRACY!", intents=discord.Intents.default())

Token = os.getenv("DISCORD_BOT_TOKEN")

VoteChannel = 1260247977075671050

Vorsitz = 1242213719795171378
Stellvertreter = 1242232096370462751

MANN = 1242196287676223538

allowedRoles = {Vorsitz, Stellvertreter}

titleOptions = discord.Option(str, name="title", description="Titel", required=True)
descriptionOption = discord.Option(str, name="description", description="Beschreibung", required=True)
ProOption = discord.Option(int, name="pro", description="Pro Stimmen", required=True)
ConOption = discord.Option(int, name="con", description="Contra Stimmen", required=True)
AbstainOption = discord.Option(int, name="abstain", description="Enthaltungen", required=True)
VoteKindOption = discord.Option(int, name="votekind", description="Art der Abstimmung 0 = Simpel, 1 = Qualified", required=True)


@bot.slash_command(
    name="debug-fixstocks",
    description="[Debug] Fix the stock market",
    guild_ids=[776823258385088552],
)
async def fixdit(ctx):
    if checkRoles(ctx):
        for compId in get_all_companies():
            set_company_value(compId[0], abs(get_company_value(compId[0])))
        await ctx.respond("Stocks fixed", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)


@bot.slash_command(
    name="debug-updatestock",
    description="[Debug] Update the stock market",
    guild_ids=[776823258385088552],
)
async def updateStock(ctx):
    if checkRoles(ctx):
        await debuGStockUpdate()
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@bot.slash_command(
    name="gamble",
    description="Gewinne Gewinne Gewinne!! TRÖT TRÖT TRÖT!!",
    guild_ids=[776823258385088552],
)
async def gamble(ctx, 
                input: discord.Option(int, name="amount", description="The amount of money you want to transfer", required=True) # type: ignore
    ):
    if input <= 0:
        await ctx.respond("You can't gamble a negative amount of money", ephemeral=True)
        return
    if get_balance(ctx.author.id) < input:
        await ctx.respond("You don't have enough money to gamble", ephemeral=True)
        return
    remove_balance(ctx.author.id, input)
    chance = getChance()
    print(chance)
    res = calcChance(chance, input)
    await ctx.respond(embed=await EmbedGenerator.generateCasinoEmbed(input, chance, res))
    add_balance(ctx.author.id, res)

@bot.slash_command(
    name="debug-addmoney",
    description="[Debug] Give money to another user",
    guild_ids=[776823258385088552],
)
async def addMoney(ctx, 
                target: discord.Option(discord.Member, name="reciever", description="The user you want to give money to", required=True), # type: ignore
                amount: discord.Option(int, name="amount", description="The amount of money you want to give", required=True) # type: ignore
    ):
    if checkRoles(ctx):
        if amount <= 0:
            await ctx.respond("You can't give a negative amount of money", ephemeral=True)
            return
        add_balance(target.id, amount)
        await ctx.respond(f"Successfully added {amount} to {target.mention}", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@bot.slash_command(
    name="debug-removemoney",
    description="[Debug] Give money to another user",
    guild_ids=[776823258385088552],
)
async def removeMoney(ctx, 
                    target: discord.Option(discord.Member, name="reciever", description="The user you want to give money to", required=True), # type: ignore
                    amount: discord.Option(int, name="amount", description="The amount of money you want to give", required=True) # type: ignore
    ):
    if checkRoles(ctx):
        if amount <= 0:
            await ctx.respond("You can't remove a negative amount of money", ephemeral=True)
            return
        remove_balance(target.id, amount)
        await ctx.respond(f"Successfully removed {amount} from {target.mention}", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@bot.slash_command(
    name="debug-setmoney",
    description="[Debug] Set Money of user",
    guild_ids=[776823258385088552],
)
async def setMoney(ctx,
                    target: discord.Option(discord.Member, name="reciever", description="The user you want to give money to", required=True), # type: ignore
                    amount: discord.Option(int, name="amount", description="The amount of money you want to give", required=True) # type: ignore
    ):
    if checkRoles(ctx):
        if amount <= 0:
            await ctx.respond("You can't set a negative amount of money", ephemeral=True)
            return
        set_user_balance(target.id, amount)
        await ctx.respond(f"Successfully set {amount} to {target.mention}", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@bot.slash_command(
    name="transfer",
    description="Transfer money to another user",
    guild_ids=[776823258385088552],
)
async def transfer(ctx,
                target: discord.Option(discord.Member, name="reciever", description="The user you want to transfer money to", required=True), # type: ignore
                amount: discord.Option(int, name="amount", description="The amount of money you want to transfer", required=True) # type: ignore
    ):
    if amount <= 0:
        await ctx.respond("You can't transfer a negative amount of money", ephemeral=True)
        return
    if get_balance(ctx.author.id) < amount:
        await ctx.respond("You don't have enough money to transfer", ephemeral=True)
        return
    transfer_balance(ctx.author.id, target.id, amount)
    await ctx.respond(f"Successfully transferred {amount} to {target.mention}", ephemeral=True)

@bot.slash_command(
    name="balance",
    description="Get your current balance",
    guild_ids=[776823258385088552],
)
async def balance(ctx):
    balance = get_balance(ctx.author.id)
    if balance is None:
        add_user(ctx.author.id, 100)
        balance = 100
    await ctx.respond(f"Your current balance is {round(balance,2)}", ephemeral=True)


@bot.slash_command(
    name="addlog",
    description="Add a log to the log channel",
    guild_ids=[776823258385088552],
)
async def AddLog(ctx,
                title: discord.Option(str, name="title", description="Titel", required=True),# type: ignore
                description: discord.Option(str, name="description", description="Beschreibung", required=True),# type: ignore
                pro: discord.Option(int, name="pro", description="Pro Stimmen", required=True),# type: ignore
                abstain: discord.Option(int, name="abstain", description="Enthaltungen", required=True),# type: ignore
                con: discord.Option(int, name="con", description="Contra Stimmen", required=True),# type: ignore
                votekind: discord.Option(int, name="votekind", description="Art der Abstimmung 0 = Simpel, 1 = Qualified", required=True)# type: ignore
                    ):
    if checkRoles(ctx):
        total = pro + con + abstain
        description = description.replace(r"\\n", "\n")
        description = f"""{description}"""
        await sendLog(await EmbedGenerator.generateLogembed(title, description, pro, con, abstain, total, votekind))
        await ctx.respond("Log added", ephemeral=True)

@bot.slash_command(
    name="startvote",
    description="Start a Vote",
    guild_ids=[776823258385088552],
)
async def startVote(ctx,
                    title: discord.Option(str, name="title", description="Titel", required=True), # type: ignore
                    description: discord.Option(str, name="description", description="Beschreibung", required=True),# type: ignore
                    votekind: discord.Option(int, name="votekind", description="Art der Abstimmung 0 = Simpel, 1 = Qualified", required=True)# type: ignore
                    ):
    if checkRoles(ctx):
        description = description.replace(r"\\n", "\n")
        description = f"""{description}"""
        voteId = VoteManager.VoteManager.getVoteManager(ctx.guild.id).startVote(title, description, votekind, [0,1])
        await sendVote(await EmbedGenerator.generateVoteEmbed(title, description, votekind), Views.VoteView(voteId, bot))
        await ctx.respond("Log added", ephemeral=True)

@bot.slash_command(
    name="test",
    description="Test",
    guild_ids=[776823258385088552],
)
async def test(ctx):
    await ctx.respond("Test", view=Views.VoteView(timeout=60))


@bot.slash_command(
    name="addconstitution",
    description="Add a new constitution",
    guild_ids=[776823258385088552],
)
async def AddConstitution(ctx):
    if checkRoles(ctx):
        await sendConstitution()
        await ctx.respond("Constitution added", ephemeral=True)

@bot.slash_command(
    name="getconstitution",
    description="get the current constitution",
    guild_ids=[776823258385088552],
)
async def GetConstitution(ctx):
    for i in constitu:
        await ctx.respond(embed=await EmbedGenerator.generateConstitutionEmbed(i["title"], i["paragraphs"]), ephemeral=True)

BotIcon = r"https://scontent-dus1-1.xx.fbcdn.net/v/t39.30808-6/327171519_1137143220327532_6078723935043886796_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=5f2048&_nc_ohc=c1WhaejPoKQQ7kNvgF0yV0S&_nc_ht=scontent-dus1-1.xx&oh=00_AYDs7F2LEexJ3HbkvIvAZ6je1bdYK4fMl2BDbAMD-L6-Tw&oe=6652E7CE"
ErgebnissIcon = r"https://images.csmonitor.com/csm/2019/02/0201-MANNESS.jpg?alias=standard_900x600"

LogChannel = 1242236502486810657

ConstitutionChannel = 1259988043327340745

def checkRoles(ctx):
    for role in ctx.author.roles:
        if role.id in allowedRoles:
            return True
    return False

async def sendConstitution():
    channel = bot.get_channel(ConstitutionChannel)
    for i in constitu:
        await channel.send(embed=await EmbedGenerator.generateConstitutionEmbed(i["title"], i["paragraphs"]))
    await sendConstitutionDivider()

async def sendConstitutionDivider():
    channel = bot.get_channel(ConstitutionChannel)
    await channel.send(embed=await EmbedGenerator.generateDividerEmbed())


async def getVoteKind(vote, pro, total):
    match vote:
        case 0:
            if pro > total/2:
                return True
            else:
                return False
        case 1:
            if pro > (total/3)*2:
                return True
            else:
                return False

async def sendLog(embed):
    channel = bot.get_channel(LogChannel)
    await channel.send(embed=embed)

async def sendVote(embed, view):
    channel = bot.get_channel(VoteChannel)
    await channel.send(f"<@&{MANN}>", embed=embed, view=view)

def applyStockChance(company_id):
    chance = genStockChance()
    if chance:
        val = get_company_value(company_id)
        new_val = val (val * chance)
        set_company_value(company_id, new_val)

    if random_bool(0.01):
        chance = -1
        return set_company_value(company_id, 0)
    return (chance, new_val)

def stockStuff():
    changeList = []
    companies = get_all_companies()
    for company in companies:
        old = get_company_value(company[0])
        stuff = applyStockChance(company[0])
        changeList.append({"name": get_company_name(company[0]), "change": round(stuff[0]*100, 2), "new": round(stuff[1], 2), "old": round(old, 2)})
    return changeList

@tasks.loop(minutes=1)
async def stockUpdate():
    now = datetime.datetime.now()
    if now.minute != 0:
        return
    channel = bot.get_channel(StockChannel)
    changeList = stockStuff()
    embeds = await EmbedGenerator.generateStockChangeEmbed(changeList)
    for embed in embeds:
        await channel.send(embed=embed)

async def debuGStockUpdate():
    channel = bot.get_channel(StockChannel)
    changeList = stockStuff()
    embeds = await EmbedGenerator.generateStockChangeEmbed(changeList)
    for embed in embeds:
        await channel.send(embed=embed)

@bot.slash_command(
    name="debug-setstock",
    description="[Debug] change Stock Value",
    guild_ids=[776823258385088552],
)
async def changeStock(ctx, 
                    company_id: discord.Option(int, name="company_id", description="Unternehmen ID", required=True), # type: ignore
                    value: discord.Option(int, name="wert", description="Der neue Wert", required=True) # type: ignore
    ):
    if checkRoles(ctx):
        set_company_value(company_id, value)
        await ctx.respond(f"Company {company_id} changed to {value}", ephemeral=True)


@bot.slash_command(
    name="debug-addcompany",
    description="[Debug] Update the stock market",
    guild_ids=[776823258385088552],
)
async def addCompany(ctx, 
                    name: discord.Option(str, name="name", description="The name of the company", required=True), # type: ignore
                    value: discord.Option(float, name="value", description="The value of the company", required=True) # type: ignore
    ):
    if checkRoles(ctx):
        add_company(name, value)
        await ctx.respond(f"Company {name} added", ephemeral=True)

@bot.slash_command(
    name="debug-removecompany",
    description="[Debug] Update the stock market",
    guild_ids=[776823258385088552],
)
async def removeCompany(ctx, 
                    company_id: discord.Option(int, name="company_id", description="The id of the company", required=True) # type: ignore
    ):
    if checkRoles(ctx):
        cur.execute("DELETE FROM companies WHERE company_id = ?", (company_id,))
        connection.commit()
        await ctx.respond(f"Company {company_id} removed", ephemeral=True)

@bot.slash_command(
    name="listcompanies",
    description="List all companies",
    guild_ids=[776823258385088552],
)
async def listCompanies(ctx):
    companies = get_all_companies()
    company_list = []
    for company in companies:
        company_list.append({"id": company[0], "name": get_company_name(company[0]), "price": round(get_company_value(company[0]),2)})
    for emb in await EmbedGenerator.generateCompanyOverviewEmbed(company_list):
        await ctx.respond(embed=emb, ephemeral=True)

@bot.slash_command(
    name="wert",
    description="Update the stock market",
    guild_ids=[776823258385088552],
)
async def wert(ctx):

    mone = getWertinEUR(get_user_balance(ctx.author.id))

    await ctx.respond(f"Du besitzt Moneten im Wert von {mone}€", ephemeral=True)


def getWertinEUR(money):
    return round((money / 1000 * halbesKilo),2)

parseTxt(open("Satzung_des_Rates_der_Manner_vom_20.5.25_3._Revision.txt", "r").readlines())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    stockUpdate.start()

bot.run(Token)