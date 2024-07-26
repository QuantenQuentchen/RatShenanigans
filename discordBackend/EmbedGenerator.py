import datetime
from discord import Embed
from VoteSystem.VoteData import Vote

BotIcon = r"https://d3i6fh83elv35t.cloudfront.net/static/2022/03/2022-03-23T224553Z_1063185917_RC2L8T9JT4FJ_RTRMADP_3_UKRAINE-CRISIS-UN-1024x683.jpg"
CapBotIcon = r"https://snworksceo.imgix.net/ids/d3a1e224-68b7-4c79-9388-e209f65026b1.sized-1000x1000.png?w=1000"
ErgebnissIcon = r"https://images.csmonitor.com/csm/2019/02/0201-MANNESS.jpg?alias=standard_900x600"
JuraBotIcon = r"https://i.pinimg.com/originals/24/3e/eb/243eeb242e6db73ff318fcbeebab726e.png"
HappyEGirl = r"https://t4.ftcdn.net/jpg/02/69/23/65/360_F_269236515_jUKu2chuA6WGl36fCqlmsw8cwGp4ICLr.jpg"
BadEgirl = r"https://c8.alamy.com/comp/2GP6D6J/disappointed-asian-teen-girl-shows-regret-pointing-and-looking-left-with-sulking-frowning-face-standing-upset-over-white-background-2GP6D6J.jpg"
enum = {
    "simple": 0,
    "qualified": 1,
}

Abstimmungsart = {
    0: "Einfache Mehrheit",
    1: "Qualifizierte Mehrheit",
}

Angenommen = {
    True: "Angenommen",
    False: "Abgelehnt",
    -1: "Ungültig",
    0: "Neuwahlen nötig",
}

chance = {
    "win": r"https://qph.cf2.quoracdn.net/main-qimg-96fae880bf4ac7dc6f33951c1a935999-lq",
    "lost": r"https://casino.betmgm.com/en/blog/wp-content/uploads/2023/09/Header-A-man-holds-his-head-in-his-hands-Biggest-gambling-losses.jpg",
    "even": r"https://image.spreadshirtmedia.com/image-server/v1/compositions/T347A2PA4306PT17X3Y5D1032852033W24621H29545/views/1,width=550,height=550,appearanceId=2,backgroundColor=000000,noPt=true/funny-poker-if-the-cards-ever-break-even-gambler-womens-t-shirt.jpg"
}

async def generateVoteEmbed(title, description, voteKind, noAbstain=False):
    embed = Embed(title=title, description=description, color=0xf400f9, type="rich", timestamp=datetime.datetime.now())
    embed.set_author(name="Democracy Bot", icon_url=BotIcon)
    embed.set_thumbnail(url=ErgebnissIcon)

    embed.add_field(name="Abstimmungsart:", value=Abstimmungsart[voteKind], inline=False)

    if(noAbstain):
        embed.add_field(name="**Das Enthaltungsrecht entfällt**", inline=False)

    return embed

async def generateLogEmbed(vote: Vote):
    if(vote.private):
        return await generateLogEmbedPrivate(vote)
    else:
        return await generateLogEmbedPublic(vote)

async def generateLogEmbedPrivate(vote: Vote):
    embed = Embed(title=vote.title, description=vote.description, color=0xf400f9, type="rich", timestamp=datetime.datetime.now())
    embed.set_author(name="Democracy Bot", icon_url=BotIcon)
    embed.set_thumbnail(url=ErgebnissIcon)

    pro = vote.getProNum()
    con = vote.getConNum()
    abstain = vote.getAbstainNum()
    total = vote.getPresentNum()

    embed.add_field(name="Abstimmungsart:", value=Abstimmungsart[vote.voteKind], inline=False)

    embed.add_field(name="Dafür:", value=f"**{pro}/{total}**", inline=False)

    if(abstain != 0):
        embed.add_field(name="Enthalten:", value=f"**{abstain}/{total}**", inline=False)

    embed.add_field(name="Dagegen:", value=f"**{con}/{total}**", inline=False)

    embed.add_field(name="Ergebniss:", value=Angenommen[vote.evaluate()], inline=False)

    return embed

async def generateLogEmbedPublic(vote: Vote):
    embed = Embed(title=vote.title, description=vote.description, color=0xf400f9, type="rich", timestamp=datetime.datetime.now())
    embed.set_author(name="Democracy Bot", icon_url=BotIcon)
    embed.set_thumbnail(url=ErgebnissIcon)

    embed.add_field(name="Abstimmungsart:", value=Abstimmungsart[vote.voteKind], inline=False)
    proStr = ""
    for votee in vote.getPro():
        proStr += f"<@{votee}> "
    
    abstainStr = ""
    for votee in vote.getAbstain():
        abstainStr += f"<@{votee}> "
    
    conStr = ""
    for votee in vote.getCon():
        conStr += f"<@{votee}> "
    if(conStr == ""):
        conStr = "Keine Stimmen"
    if(abstainStr == ""):
        abstainStr = "Keine Stimmen"
    if(proStr == ""):
        proStr = "Keine Stimmen"

    embed.add_field(name="Dafür:", value=f"**{proStr}**", inline=False)

    if(vote.getAbstainNum() != 0):
        embed.add_field(name="Enthalten:", value=f"**{abstainStr}**", inline=False)

    embed.add_field(name="Dagegen:", value=f"**{conStr}**", inline=False)

    embed.add_field(name="Ergebniss:", value=Angenommen[vote.evaluate()], inline=False)

    return embed

async def generateMemoryQuestionEmbed(question: str):
    embed = Embed(title=question, description="", color=0x1d05fa, type="rich", timestamp=datetime.datetime.now())
    embed.set_author(name="Jura Bot", icon_url=JuraBotIcon)
    return embed

async def generateMemoryAnswerEmbed(question, answer):
    embed = Embed(title=question, description=answer, color=0x1d05fa, type="rich", timestamp=datetime.datetime.now())
    embed.set_author(name="Jura Bot", icon_url=JuraBotIcon)
    embed.set_image(url=HappyEGirl)
    return embed

async def generateMemoryTimeoutEmbed():
    embed = Embed(title="Timeout", description="Du hast zu lange gebraucht, du fucking Looser, und du bist black", color=0x1d05fa, type="rich", timestamp=datetime.datetime.now())
    embed.set_author(name="Jura Bot", icon_url=JuraBotIcon)
    embed.set_image(url=BadEgirl)
    return embed

async def generateDividerEmbed():
    embed = Embed(title=f"Aktuelle Satzung von {datetime.datetime.now().strftime('%Y/%m/%d, %H:%M')}", description="", color=0x05a4fa, type="rich")
    embed.set_author(name="Democracy Bot", icon_url=BotIcon)
    return embed

async def generateConstitutionEmbed(title, Content):
    embed = Embed(title=title, description="", color=0x1d05fa, type="rich", timestamp=datetime.datetime.now())
    embed.set_author(name="Democracy Bot", icon_url=BotIcon)
    for art in Content:
        embed.add_field(name=art["title"], value=art["content"], inline=False)
    return embed

async def generateLogembed(title, description, pro, con, abstain, total, voteKind):
    embed = Embed(title=title, description=description, color=0xf400f9, type="rich", timestamp=datetime.datetime.now())
    embed.set_author(name="Democracy Bot", icon_url=BotIcon)
    embed.set_thumbnail(url=ErgebnissIcon)

    embed.add_field(name="Abstimmungsart:", value=Abstimmungsart[voteKind], inline=False)

    embed.add_field(name="Dafür:", value=f"**{pro}/{total}**", inline=False)

    if(abstain != 0):
        embed.add_field(name="Enthalten:", value=f"**{abstain}/{total}**", inline=False)

    embed.add_field(name="Dagegen:", value=f"**{con}/{total}**", inline=False)

    embed.add_field(name="Ergebniss:", value=Angenommen[await getVoteKind(voteKind, pro, total)], inline=False)

    return embed

async def generateCasinoEmbed(input, res, win):

    winText = ""

    img = r""
    if res == -1:
        img = chance["lost"]
        winText = "alles Verloren, better luck next time."
    elif chance == 0:
        img = chance["even"]
        winText = "bist gerade so mit deinem Einsatz wieder raus gekommen."
    else:
        img = chance["win"]
        winText = f"{win}M gewonnen, Glückwunsch."

    embed = Embed(title="Casino", description=f"Du hast {input} eingezahlt und {winText}", color=0x1d05fa, type="rich", timestamp=datetime.datetime.now())
    embed.set_author(name="Capitalism Bot", icon_url=CapBotIcon)
    embed.set_image(url=img)
    return embed

def getGenericStockChangeEmbed():
    embed = Embed(title="Die Freie Hand des Marktes greift dir langsam in den Schritt", description="Markt Stuff", color=0x1d05fa, type="rich", timestamp=datetime.datetime.now())
    embed.set_author(name="Capitalism Bot", icon_url=CapBotIcon)
    return embed

async def generateStockChangeEmbed(stocks):
    retList = []
    currEmbed = getGenericStockChangeEmbed()
    for idx, stock in enumerate(stocks, start=1):  # Start counting from 1
        currEmbed.add_field(name=f"{stock['name']} Alt: {stock['old']}, Neu: {stock['new']}, Änderung {stock['change']}%", value="", inline=False)
        if idx % 25 == 0:
            retList.append(currEmbed)
            currEmbed = getGenericStockChangeEmbed()
    if currEmbed.fields:  # Check if there are any fields added to the last embed
        retList.append(currEmbed)
    return retList
#d

def getGerneriCompanyOverviewEmbed():
    embed = Embed(title="Cringe Club", description="Markt Stuff", color=0x1d05fa, type="rich", timestamp=datetime.datetime.now())
    embed.set_author(name="Capitalism Bot", icon_url=CapBotIcon)
    return embed

async def generateCompanyOverviewEmbed(companies):
    retList = []
    currEmbed = getGerneriCompanyOverviewEmbed()
    for idx, company in enumerate(companies, start=1):  # Start counting from 1
        currEmbed.add_field(name=f"**{company['name'].upper()}**: {company['price']}M ({company['id']})", value="", inline=False)
        if idx % 25 == 0:
            retList.append(currEmbed)
            currEmbed = getGerneriCompanyOverviewEmbed()
    if currEmbed.fields:  # Check if there are any fields added to the last embed
        retList.append(currEmbed)
    return retList

async def generateCompanyUserOverviewEmbed(companies):
    retList = []
    currEmbed = getGerneriCompanyOverviewEmbed()
    for idx, company in enumerate(companies, start=1):  # Start counting from 1
        currEmbed.add_field(name=f"**{company['name'].upper()}**: {company['price']}M x {company['num']} = {company['price']*company['num']}M", value="", inline=False)
        if idx % 25 == 0:
            retList.append(currEmbed)
            currEmbed = getGerneriCompanyOverviewEmbed()
    if currEmbed.fields:  # Check if there are any fields added to the last embed
        retList.append(currEmbed)
    return retList

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