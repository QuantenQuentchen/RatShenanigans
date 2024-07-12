from Backend.databaseManager import dbManager
from discordBackend.privilegeManager import privilegeManager
from discordBackend.BotManager import BotManager
import discord

privMen = privilegeManager.getInstance()

bot = BotManager.getBot()

MichiID = 546434993690247191
dbM = dbManager.getInstance()

@bot.slash_command(
    name="addmemory",
    description="Add Memory to Michi",
    guild_ids=[776823258385088552],
)
async def addMemory(ctx,
                    ques: discord.Option(str, name="question", description="The question you want to add", required=True), # type: ignore
                    answer: discord.Option(str, name="answer", description="The answer to the question", required=True) # type: ignore
                    ):
    print("Checking Memory")
    if privMen.isMemoryGuy(ctx.author):
        dbM.add_memory(ques, answer)
        await ctx.respond(f"Successfully added memory to Michi", ephemeral=True)
    else:
        await ctx.respond(f"Only Michi can add memory to Michi", ephemeral=True)

