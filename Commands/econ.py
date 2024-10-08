import discord

import discordBackend.EmbedGenerator as EmbedGenerator
from Backend.databaseManager import dbManager
from Economy.manage import get_balance, add_balance, remove_balance, transfer_balance, getWertinEUR
from Economy.math import getChance, calcChance
from discordBackend.BotManager import BotManager

econ = BotManager.getBot().create_group("econ", "Economy commands")

dbM = dbManager.getInstance()

@econ.command(
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

@econ.command(
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

@econ.command(
    name="balance",
    description="Get your current balance",
    guild_ids=[776823258385088552],
)
async def balance(ctx):
    balance = get_balance(ctx.author.id)
    await ctx.respond(f"Your current balance is {round(balance,2)}", ephemeral=True)

@econ.command(
    name="listcompanies",
    description="List all companies",
    guild_ids=[776823258385088552],
)
async def listCompanies(ctx):
    companies = dbM.get_all_companies()
    company_list = []
    for company in companies:
        company_list.append({"id": company[0], "name": dbM.get_company_name(company[0]), "price": round(dbM.get_company_value(company[0]),2)})
    for emb in await EmbedGenerator.generateCompanyOverviewEmbed(company_list):
        await ctx.respond(embed=emb, ephemeral=True)

@econ.command(
    name="wert",
    description="Update the stock market",
    guild_ids=[776823258385088552],
)
async def wert(ctx):

    mone = getWertinEUR(dbM.get_user_balance(ctx.author.id))

    await ctx.respond(f"Du besitzt Moneten im Wert von {mone}€", ephemeral=True)

async def getcompanyNames(ctx: discord.AutocompleteContext):
    print("getcompanyNames")
    companyNames= []
    for company in dbM.get_all_companies():
        companyNames.append(dbM.get_company_name(company[0]))
    return companyNames

@econ.command(
    name="buystock",
    description="Buy your stocks, engage in unprotected Capitalism",
    guild_ids=[776823258385088552],
)
async def buystocks(ctx,
                    companyname: discord.Option(str, autocomplete= discord.utils.basic_autocomplete(getcompanyNames)), # type: ignore
                    number: discord.Option(int), # type: ignore
                    ):
    companyID= dbM.get_company_id(companyname)
    value= dbM.get_company_value(companyID)

    if number<=0:
        await ctx.respond("DU KANNST NICHT NEGATIVE AKTIEN KAUFEN DU IDIOT")
        return

    if get_balance(ctx.author.id)< value*number:
        await ctx.respond("DU BIST GERINGVERDIENER, DU KANNST DIR NICHT MAL DAS KACKEN LEISTEN")
        return  
    dbM.add_stocks_to_user(ctx.author.id, companyID, number)
    remove_balance(ctx.author.id, value*number)
    await ctx.respond("DU BIST NUN TEIL DES KAPITALISTISCHEN SYSTEMS. HERZLICHEN GLÜCKWUNSCH!")
    return

@econ.command(
    name="liststocks",
    description="Hier eine anzahl an Kaufoptionen",
    guild_ids=[776823258385088552]
)
async def liststocks(ctx):
    broke= dbM.get_all_user_stocks(ctx.author.id)
    diesdas = []
    for stock in broke:
        diesdas.append({"name": dbM.get_company_name(stock[0]), "num": stock[1], "price": round(dbM.get_company_value(stock[0]),2)})
    print(diesdas)
    embeds = await EmbedGenerator.generateCompanyUserOverviewEmbed(diesdas)
    for emb in embeds:
        await ctx.respond(embed=emb, ephemeral=True)


@econ.command(
    name="sellstock",
    description="Buy your stocks, engage in unprotected Capitalism",
    guild_ids=[776823258385088552],
)
async def sellstocks(ctx,
                    companyname: discord.Option(str, autocomplete= discord.utils.basic_autocomplete(getcompanyNames)), # type: ignore
                    number: discord.Option(int), # type: ignore
                    ):
    companyID= dbM.get_company_id(companyname)
    value= dbM.get_company_value(companyID)
    if number<=0:
        await ctx.respond("DU KANNST NICHT NEGATIVE AKTIEN VERKAUFEN DU IDIOT")
        return
    
    if dbM.get_user_stocks(ctx.author.id, companyID)==0:
        await ctx.respond("DU HAST KEINE AKTIEN DU ARMES SCHWEIN")
        return

    if dbM.get_user_stocks(ctx.author.id, companyID)< number:
        await ctx.respond("DU HAST NICHT GENUG AKTIEN DU ARMES SCHWEIN")
        return
    dbM.remove_stocks_from_user(ctx.author.id, companyID, number)
    add_balance(ctx.author.id, value*number)
    await ctx.respond("DU HAST DEINE SEELE VERKAUFT. GUT GEMACHT!")
    return