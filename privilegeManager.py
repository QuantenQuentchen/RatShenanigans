

class privilegeManager:

    insance = None
    def getInstance():
        if privilegeManager.insance is None:
            privilegeManager.insance = privilegeManager()
        return privilegeManager.insance


    def __init__(self):

        AHHHH = 704975440963698768

        oneTrueAdmin = 1260632825527402606
        Vorsitz = 1242213719795171378
        Stellvertreter = 1242232096370462751
        MANN = 1242196287676223538

        self.adminRoles = {oneTrueAdmin}
        self.vorsitz = {Vorsitz, Stellvertreter}
        self.MANN = {MANN}
        self.everyone = set()
        self.exclude = {AHHHH}

    def init(self):
        pass

    def mentionMANN(self):
        str = ""
        for role in self.MANN:
            str += "<@&" + str(role) + ">,"
        return str[:-1]
    
    def mentionVorsitz(self):
        str = ""
        for role in self.vorsitz:
            str += "<@&" + str(role) + ">,"
        return str[:-1]
    
    def mentionAdmin(self):
        str = ""
        for role in self.adminRoles:
            str += "<@&" + str(role) + ">,"
        return str[:-1]

    def isEveryone(self, memberRoles) -> bool:
        return not any(role in self.exclude for role in memberRoles)

    def isVorsitz(self, memberRoles) -> bool:
        return any(role in self.vorsitz or role in self.adminRoles for role in memberRoles) and not any(role in self.exclude for role in memberRoles)

    def isMANN(self, memberRoles) -> bool:
        return any(role in self.MANN or role in self.vorsitz or role in self.adminRoles for role in memberRoles) and not any(role in self.exclude for role in memberRoles)
