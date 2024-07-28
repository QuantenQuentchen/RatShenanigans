

class privilegeManager:

    insance = None
    def getInstance():
        if privilegeManager.insance is None:
            privilegeManager.insance = privilegeManager()
        return privilegeManager.insance


    def __init__(self):

        #Hardcoded Roles


        #Excluded user ID, ie. the "owner"
        AHHHH = 704975440963698768

        #Admin Role
        oneTrueAdmin = 1260632825527402606
        
        Vorsitz = 1242213719795171378
        Stellvertreter = 1242232096370462751
        MANN = 1242196287676223538

        #For that one guy who wants to memorize stuff
        self.MemoryGuy = 546434993690247191

        self.Furry = 315880867597910018

        self.Schewaun = 715629325654949998

        self.Kevin = 508365874223251457

        #Compiled lists from literals
        self.adminRoles = {oneTrueAdmin}
        self.vorsitz = {Vorsitz, Stellvertreter}
        self.MANN = {MANN}
        self.everyone = set() #currently empty as I don't know what constitutes an everyone role, also never actually used except in cascasding role checks, ie. currently no one is everyone also it's never checker wether someone is everyone
        self.exclude = {AHHHH}

    def init(self):
        pass

    def __checkUserId__(self, author, ids: set):
        return author.id in ids

    def __checkUserRoles__(self, author, roles):
        return any(role.id in roles for role in author.roles)

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

    def isEveryone(self, member) -> bool:
        return not self.__checkUserId__(member, self.exclude)

    def isVorsitz(self, member) -> bool:
        return self.__checkUserRoles__(member, self.vorsitz) or self.isAdmin(member) and self.isEveryone(member)

    def isMANN(self, member) -> bool:
        return self.__checkUserRoles__(member, self.MANN) or self.isVorsitz(member) and self.isEveryone(member)
    
    def isAdmin(self, member) -> bool:
        return self.__checkUserRoles__(member, self.adminRoles) and self.isEveryone(member)

    def isMemoryGuy(self, member) -> bool:
        return member.id == self.MemoryGuy
    
    def isFurry(self, member) -> bool:
        return member.id == self.Furry
    
    def isSchewaun(self, member) -> bool:
        return member.id == self.Schewaun

    def isKevin(self, member) -> bool:
        return member.id == self.Kevin