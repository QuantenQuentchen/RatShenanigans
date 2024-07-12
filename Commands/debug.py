from discord import Option, Member, SlashCommandGroup


from Backend.databaseManager import dbManager
from discordBackend.privilegeManager import privilegeManager
from discordBackend.BotManager import BotManager

debug = BotManager.getBot().create_group("debug", "Finger WECH!")

dbM = dbManager.getInstance()
privMen = privilegeManager.getInstance()

@debug.command(
    name="fixstocks",
    description="[Debug] Fix the stock market",
    guild_ids=[776823258385088552],
)
async def fixdit(ctx):
    if privMen.isVorsitz(ctx.author):
        for compId in dbM.get_all_companies():
            dbM.set_company_value(compId[0], abs(dbM.get_company_value(compId[0])))
        await ctx.respond("Stocks fixed", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)


@debug.command(
    name="updatestock",
    description="[Debug] Update the stock market",
    guild_ids=[776823258385088552],
)
async def updateStock(ctx):
    if privMen.isVorsitz(ctx.author):
        await dbM.debuGStockUpdate()
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@debug.command(
    name="addmoney",
    description="[Debug] Give money to another user",
    guild_ids=[776823258385088552],
)
async def addMoney(ctx, 
                target: Option(Member, name="reciever", description="The user you want to give money to", required=True), # type: ignore
                amount: Option(int, name="amount", description="The amount of money you want to give", required=True) # type: ignore
    ):
    if privMen.isVorsitz(ctx.author):
        if amount <= 0:
            await ctx.respond("You can't give a negative amount of money", ephemeral=True)
            return
        dbM.add_balance(target.id, amount)
        await ctx.respond(f"Successfully added {amount} to {target.mention}", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@debug.command(
    name="removemoney",
    description="[Debug] Give money to another user",
    guild_ids=[776823258385088552],
)
async def removeMoney(ctx, 
                    target: Option(Member, name="reciever", description="The user you want to give money to", required=True), # type: ignore
                    amount: Option(int, name="amount", description="The amount of money you want to give", required=True) # type: ignore
    ):
    if privMen.isVorsitz(ctx.author):
        if amount <= 0:
            await ctx.respond("You can't remove a negative amount of money", ephemeral=True)
            return
        dbM.remove_balance(target.id, amount)
        await ctx.respond(f"Successfully removed {amount} from {target.mention}", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@debug.command(
    name="setmoney",
    description="[Debug] Set Money of user",
    guild_ids=[776823258385088552],
)
async def setMoney(ctx,
                    target: Option(Member, name="reciever", description="The user you want to give money to", required=True), # type: ignore
                    amount: Option(int, name="amount", description="The amount of money you want to give", required=True) # type: ignore
    ):
    if privMen.isVorsitz(ctx.author):
        if amount <= 0:
            await ctx.respond("You can't set a negative amount of money", ephemeral=True)
            return
        dbM.set_user_balance(target.id, amount)
        await ctx.respond(f"Successfully set {amount} to {target.mention}", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@debug.command(
    name="setstock",
    description="[Debug] change Stock Value",
    guild_ids=[776823258385088552],
)
async def changeStock(ctx, 
                    company_id: Option(int, name="company_id", description="Unternehmen ID", required=True), # type: ignore
                    value: Option(int, name="wert", description="Der neue Wert", required=True) # type: ignore
    ):
    if privMen.isVorsitz(ctx.author):
        dbM.set_company_value(company_id, value)
        await ctx.respond(f"Company {company_id} changed to {value}", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@debug.command(
    name="addcompany",
    description="[Debug] Update the stock market",
    guild_ids=[776823258385088552],
)
async def addCompany(ctx, 
                    name: Option(str, name="name", description="The name of the company", required=True), # type: ignore
                    value: Option(float, name="value", description="The value of the company", required=True) # type: ignore
    ):
    if privMen.isVorsitz(ctx.author):
        dbM.add_company(name, value)
        await ctx.respond(f"Company {name} added", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@debug.command(
    name="removecompany",
    description="[Debug] Update the stock market",
    guild_ids=[776823258385088552],
)
async def removeCompany(ctx, 
                    company_id: Option(int, name="company_id", description="The id of the company", required=True) # type: ignore
    ):
    if privMen.isVorsitz(ctx.author):
        dbM.remove_company(company_id)
        await ctx.respond(f"Company {company_id} removed", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)