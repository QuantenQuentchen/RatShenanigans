from databaseManager import dbManager

class constitutionManager():

    instances = {}
    @staticmethod
    def getConstitutionManager(guildID):
        if guildID not in constitutionManager.instances:
            constitutionManager.instances[guildID] = constitutionManager(guildID)
        return constitutionManager.instances[guildID]

    def parseTxt(self, txt):
        currentArticel = {}
        currentParagraph = {"title": "", "content": ""}
        for line in txt:
            if len(line) == 0:
                continue
            if line.startswith("Artikel"):
                line = line.replace("\n", "")
                line = line.replace("\t", "")
                if(len(currentArticel) != 0):
                    self.constitution.append(currentArticel)
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
        for i in self.constitution:
            i["paragraphs"] = [paragraph for paragraph in i["paragraphs"] if not (paragraph.get("title") == "" and paragraph.get("content") == "")]

    def __init__(self, guildID):
        self.constitution = []
        self.guildID = guildID
        self.dbM = dbManager.getInstance()
        for art_id in self.dbM.get_all_articleIDs():
            art = self.dbM.get_article(art_id[0])
            self.constitution.append({"title": f"Artikel {art['num']} {art['title'][0][0]}:", "paragraphs": art["paragraphs"]})

    def getConstitution(self):
        return self.constitution