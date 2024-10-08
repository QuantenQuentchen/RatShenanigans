import discord

import discordBackend.EmbedGenerator as EmbedGenerator
from VoteSystem.VoteManager import VoteManager
from discordBackend.privilegeManager import privilegeManager
from discordBackend.ChannelManager import ChannelManager
import discordBackend.Views as Views
from Government.constitutionManager import constitutionManager
from discordBackend.BotManager import BotManager
from volatileStateHandler import VolatileStateHandler
from Backend.prefManager import PrefManager

#Creates command group
govern = BotManager.getBot().create_group("govern", "Government commands")

privMen = privilegeManager.getInstance()

bot = BotManager.getBot()

async def sendConstitution(ctx):
    for i in constitutionManager.getConstitutionManager(ctx.guild.id).getConstitution():
        await ChannelManager.getInstance(ctx.guild.id).sendOnConstitutionChannel(embed=await EmbedGenerator.generateConstitutionEmbed(i["title"], i["paragraphs"]))
    await sendConstitutionDivider(ctx)

async def sendConstitutionDivider(ctx):
    await ChannelManager.getInstance(ctx.guild.id).sendOnConstitutionChannel(embed=await EmbedGenerator.generateDividerEmbed())

#sets this at command for the group
@govern.command(
    name="addlog",
    description="Add a log to the log channel",
    guild_ids=[776823258385088552],
)
async def AddLog(ctx,
                title: discord.Option(str, name="title", description="Titel", required=True),# type: ignore (ignore to ignore erronious pylance type error) defines the inputs for the slash command
                description: discord.Option(str, name="description", description="Beschreibung", required=True),# type: ignore
                pro: discord.Option(int, name="pro", description="Pro Stimmen", required=True),# type: ignore
                abstain: discord.Option(int, name="abstain", description="Enthaltungen", required=True),# type: ignore
                con: discord.Option(int, name="con", description="Contra Stimmen", required=True),# type: ignore
                votekind: discord.Option(int, name="votekind", description="Art der Abstimmung 0 = Simpel, 1 = Qualified", required=True)# type: ignore
                    ):
    if privMen.isVorsitz(ctx.author):
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
    if privMen.isVorsitz(ctx.author):
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
    if privMen.isVorsitz(ctx.author):
        await sendConstitution()
        await ctx.respond("Constitution added", ephemeral=True)

@govern.command(
    name="setstockupdate",
    description="Set the stock update state",
    guild_ids=[776823258385088552],
)
async def setStockUpdate(ctx,
                        state: discord.Option(bool, name="state", description="State", required=True) # type: ignore
                        ):
        if privMen.isVorsitz(ctx.author):
            VolatileStateHandler.getInstance().setDoMarket(state)
            await ctx.respond("Stock Update state set", ephemeral=True)

@govern.command(
    name="setstockchannel",
    description="Set the stock channel",
    guild_ids=[776823258385088552],
)
async def setStockChannel(ctx,
                        channel: discord.Option(discord.abc.GuildChannel, name="channel", description="Channel", required=True) # type: ignore
                        ):
        if privMen.isVorsitz(ctx.author):
            PrefManager.getInstance().set_channel(PrefManager.kind.Stock, ctx.guild.id, channel.id)
            await ctx.respond("Stock Channel set", ephemeral=True)
        else:
            await ctx.respond("Nah you don't", ephemeral=True)

@govern.command(
    name="setvotechannel",
    description="Set the vote channel",
    guild_ids=[776823258385088552],
)
async def setVoteChannel(ctx,
                        channel: discord.Option(discord.abc.GuildChannel, name="channel", description="Channel", required=True) # type: ignore
                        ):
        if privMen.isVorsitz(ctx.author):
            PrefManager.getInstance().set_channel(PrefManager.kind.Vote, ctx.guild.id, channel.id)
            await ctx.respond("Vote Channel set", ephemeral=True)
        else:
            await ctx.respond("Nah you don't", ephemeral=True)

@govern.command(
    name="setlogchannel",
    description="Set the log channel",
    guild_ids=[776823258385088552],
)
async def setLogChannel(ctx,
                        channel: discord.Option(discord.abc.GuildChannel, name="channel", description="Channel", required=True) # type: ignore
                        ):
        if privMen.isVorsitz(ctx.author):
            PrefManager.getInstance().set_channel(PrefManager.kind.Log, ctx.guild.id, channel.id)
            await ctx.respond("Log Channel set", ephemeral=True)
        else:
            await ctx.respond("Nah you don't", ephemeral=True)

@govern.command(
    name="setconstitutionchannel",
    description="Set the constitution channel",
    guild_ids=[776823258385088552],
)
async def setConstitutionChannel(ctx,
                        channel: discord.Option(discord.abc.GuildChannel, name="channel", description="Channel", required=True) # type: ignore
                        ):
        if privMen.isVorsitz(ctx.author):
            PrefManager.getInstance().set_channel(PrefManager.kind.Constitution, ctx.guild.id, channel.id)
            await ctx.respond("Constitution Channel set", ephemeral=True)
        else:
            await ctx.respond("Nah you don't", ephemeral=True)