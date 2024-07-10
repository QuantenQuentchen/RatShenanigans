import discord
from VoteManager import VoteManager as VoteManager
import EmbedGenerator as EmbedGenerator

LogChannel = 1242236502486810657

ConstitutionChannel = 1259988043327340745

Vorsitz = 1242213719795171378
Stellvertreter = 1242232096370462751
MANN = 1242196287676223538

VoteChannel = 1260247977075671050



allowedRoles = {Vorsitz, Stellvertreter, MANN}

def checkRole(member: discord.Member):
    for role in member.roles:
        if role.id in allowedRoles:
            return True
    return False


async def sendVote(bot, embed, view):
    channel = bot.get_channel(VoteChannel)
    await channel.send(f"<@&{MANN}>", embed=embed, view=view)


async def startNoAbstainVote(vote, guildID, bot):
        description = vote.description
        title = vote.title
        votekind = vote.voteKind
        voteId = VoteManager.getVoteManager(guildID).startVote(title, description, votekind, [0,1])
        await sendVote(await EmbedGenerator.generateVoteEmbed(title, description, votekind), VoteView(voteId, bot, True))

class VoteView(discord.ui.View):

    def __init__(self, voteID: int, bot: discord.Client, noAbstain: bool = False):
        super().__init__(timeout=30)
        self.bot = bot
        self.voteID = voteID
        self.noAbstain = noAbstain

    async def sendLog(self, embed):
        channel = self.bot.get_channel(LogChannel)
        await channel.send(embed=embed)

    def add_item(self, item):
        # Check if the item is the button to conditionally disable
        if isinstance(item, discord.ui.Button) and item.label == "Enthaltung":
            item.disabled = self.noAbstain
        super().add_item(item)

    async def on_timeout(self):
        self.disable_all_items()
        
        for item in self.children:
            self.remove_item(item)
        
        self.add_item(discord.ui.Button(label="Vote Beendet", style=discord.ButtonStyle.grey, disabled=True))
        await self.sendLog(await EmbedGenerator.generateLogEmbed(VoteManager.getVoteManager(self.message.guild.id).getVote(self.voteID)))
        await self.message.edit(view=self)
        if(VoteManager.getVoteManager(self.message.guild.id).getVote(self.voteID).evaluate() == 0):
            await startNoAbstainVote(VoteManager.getVoteManager(self.message.guild.id).getVote(self.voteID), self.message.guild.id, self.bot)
        print("Timeout")

    @discord.ui.button(label="Pro", style=discord.ButtonStyle.green)
    async def pro(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not checkRole(interaction.user):
            await interaction.response.send_message("You are not allowed to vote", ephemeral=True)
            return
        
        VoteManager.getVoteManager(interaction.guild.id).getVote(self.voteID).addPro(interaction.user.id)

        await interaction.response.send_message("Voted Pro", ephemeral=True)
    
    @discord.ui.button(label="Enthaltung", style=discord.ButtonStyle.grey)
    async def abstain(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not checkRole(interaction.user):
            await interaction.response.send_message("You are not allowed to vote", ephemeral=True)
            return
        if self.noAbstain:
            await interaction.response.send_message("Das Enthaltungsrecht entfällt", ephemeral=True)
            button.disabled = True
            return
        
        VoteManager.getVoteManager(interaction.guild.id).getVote(self.voteID).addAbstain(interaction.user.id)

        await interaction.response.send_message("Voted Abstain", ephemeral=True)
    
    @discord.ui.button(label="Con", style=discord.ButtonStyle.red)
    async def contra(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not checkRole(interaction.user):
            await interaction.response.send_message("You are not allowed to vote", ephemeral=True)
            return
        
        VoteManager.getVoteManager(interaction.guild.id).getVote(self.voteID).addCon(interaction.user.id)

        await interaction.response.send_message("Voted Con", ephemeral=True)
