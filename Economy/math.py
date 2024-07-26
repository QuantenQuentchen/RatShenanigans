import random
import math

base = 6.52

halbesKilo = (base/53)*50

wertvon1kEUR = halbesKilo

chanceArr = []

#Generates a list of chances for gambling to have at least somewhat uniform odds
for i in range(70):
    chanceArr.append(-1) #Fail

for i in range(25):
    chanceArr.append(0) #Break even

for i in range(4):
    chanceArr.append([1.1, 3.0]) #Generate random multiplier between these values

chanceArr.append(4) #4x Win


def random_bool(true_percentage):
    #Returns true with a certain percentage
    return random.random() < true_percentage / 100.0

def genStockChance():
    mu = 0
    sigma = -.1
    return random.gauss(mu, sigma) 
    #generates random float

def round_up(value, digits):
    #roundup helper function sometimes used somethines not
    scale = 10 ** digits
    return math.ceil(value * scale) / scale

def getChance():
    #Btw ich sollte docstrings schreiben aber ahhhh neeee
    #Chance for Gambling
    choice = random.choice(chanceArr)
    if type(choice) == int:
        return choice
    else:
        return random.uniform(choice[0], choice[1])

def calcChance(chance, input):
    res = chance
    result = round_up(input*res, 2)
    if res == -1:
        result = 0
    if res == 0:
        result = input
    return result