from discord import SlashCommandGroup

from Government.constitutionManager import constitutionManager
import EmbedGenerator
from BotManager import BotManager


rat = BotManager.getBot().create_group("rat", "Mitglieder des Rates")

@rat.command(
    name="getconstitution",
    description="get the current constitution",
    guild_ids=[776823258385088552],
)
async def GetConstitution(ctx):
    for i in constitutionManager.getConstitutionManager(ctx.guild.id).getConstitution():
        await ctx.respond(embed=await EmbedGenerator.generateConstitutionEmbed(i["title"], i["paragraphs"]), ephemeral=True)