from discord import Option, Member, SlashCommandGroup


from Backend.databaseManager import dbManager
from discordBackend.privilegeManager import privilegeManager
from discordBackend.BotManager import BotManager
from volatileStateHandler import VolatileStateHandler

hatecrime = BotManager.getBot().create_group("hatecrime", "Funy")

dbM = dbManager.getInstance()
privMen = privilegeManager.getInstance()
volStateHan = VolatileStateHandler.getInstance()

@hatecrime.command(
    name="peggingmode",
    description="[Hatecrime] Michi mags",
    guild_ids=[776823258385088552],
)
async def peggingMode(ctx,
                    mode: Option(bool, name="mode", description="The mode you want to set", required=True) # type: ignore
    ):
    if privMen.isAdmin(ctx.author):
        volStateHan.setFunny(mode)
        await ctx.respond(f"Pegging mode set to {mode}", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@hatecrime.command(
    name="furrymode",
    description="[Hatecrime] Däniel mags",
    guild_ids=[776823258385088552],
)
async def furryMode(ctx,
                    mode: Option(bool, name="mode", description="The mode you want to set", required=True) # type: ignore
    ):
    if privMen.isAdmin(ctx.author):
        volStateHan.setFurry(mode)
        await ctx.respond(f"Furry mode set to {mode}", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@hatecrime.command(
    name="schewaunmode",
    description="[Hatecrime] Schewaun mags",
    guild_ids=[776823258385088552],
)
async def schewaunMode(ctx,
                    mode: Option(bool, name="mode", description="The mode you want to set", required=True) # type: ignore
    ):
    if privMen.isAdmin(ctx.author):
        volStateHan.setDonAsk(mode)
        await ctx.respond(f"Schewaun mode set to {mode}", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)

@hatecrime.command(
    name="kevinmode",
    description="[Hatecrime] Fick dich",
    guild_ids=[776823258385088552],
)
async def kevinMode(ctx,
                    mode: Option(bool, name="mode", description="The mode you want to set", required=True) # type: ignore
    ):
    if privMen.isAdmin(ctx.author) or privMen.isVorsitz(ctx.author):
        volStateHan.setKevin(mode)
        await ctx.respond(f"Kevin mode set to {mode}", ephemeral=True)
    else:
        await ctx.respond("You are not allowed to use this command", ephemeral=True)