import discord

import EmbedGenerator as EmbedGenerator
from VoteManager import VoteManager
from privilegeManager import privilegeManager
from ChannelManager import ChannelManager
import Views
from Government.constitutionManager import constitutionManager
from BotManager import BotManager

govern = BotManager.getBot().create_group("govern", "Government commands")

privMen = privilegeManager.getInstance()

bot = BotManager.getBot()

async def sendConstitution(ctx):
    for i in constitutionManager.getConstitutionManager(ctx.guild.id).getConstitution():
        await ChannelManager.getInstance(ctx.guild.id).sendOnConstitutionChannel(embed=await EmbedGenerator.generateConstitutionEmbed(i["title"], i["paragraphs"]))
    await sendConstitutionDivider(ctx)

async def sendConstitutionDivider(ctx):
    await ChannelManager.getInstance(ctx.guild.id).sendOnConstitutionChannel(embed=await EmbedGenerator.generateDividerEmbed())

@govern.command(
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
    if privMen.isVorsitz(ctx.author.roles):
        total = pro + con + abstain
        description = description.replace(r"\\n", "\n")
        description = f"""{description}"""
        await ChannelManager.getInstance(ctx.guild.id).sendOnLogChannel(embed=await EmbedGenerator.generateLogembed(title, description, pro, con, abstain, total, votekind))
        await ctx.respond("Log added", ephemeral=True)
    else:
        await ctx.respond("du hast keine Rechte, du Frau", ephemeral=True)

@govern.command(
    name="startvote",
    description="Start a Vote",
    guild_ids=[776823258385088552],
)
async def startVote(ctx,
                    title: discord.Option(str, name="title", description="Titel", required=True), # type: ignore
                    description: discord.Option(str, name="description", description="Beschreibung", required=True),# type: ignore
                    votekind: discord.Option(int, name="votekind", description="Art der Abstimmung 0 = Simpel, 1 = Qualified", required=True)# type: ignore
                    ):
    if privMen.isVorsitz(ctx.author.roles):
        description = description.replace(r"\\n", "\n")
        description = f"""{description}"""
        voteId = VoteManager.getVoteManager(ctx.guild.id).startVote(title, description, votekind, [0,1])
        await ChannelManager.getInstance(ctx.guild.id).sendOnVoteChannel(embed = await EmbedGenerator.generateVoteEmbed(title, description, votekind), view = Views.VoteView(voteId, bot))
        await ctx.respond("Log added", ephemeral=True)

@govern.command(
    name="addconstitution",
    description="Add a new constitution",
    guild_ids=[776823258385088552],
)
async def AddConstitution(ctx):
    if privMen.isVorsitz(ctx.author.roles):
        await sendConstitution()
        await ctx.respond("Constitution added", ephemeral=True)