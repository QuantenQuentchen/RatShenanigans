import random
import math

base = 6.52

halbesKilo = (base/53)*50

wertvon1kEUR = halbesKilo

chanceArr = []

for i in range(70):
    chanceArr.append(-1)

for i in range(25):
    chanceArr.append(0)

for i in range(4):
    chanceArr.append([1.1, 3.0])

chanceArr.append(4)


def random_bool(true_percentage):
    return random.random() < true_percentage / 100.0

def genStockChance():
    return random.uniform(-0.9, 3.0)

def round_up(value, digits):
    scale = 10 ** digits
    return math.ceil(value * scale) / scale

def getChance():
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