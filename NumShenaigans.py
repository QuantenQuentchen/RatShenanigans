def humanize(inpt):
    inpt = round(inpt, 2)
    if inpt >= 1000000000:
        return str(round(inpt/1000000000, 12)) + 'B'
    elif inpt >= 1000000:
        return str(round(inpt/1000000, 9)) + 'M'
    elif inpt >= 1000:
        return str(round(inpt/1000, 6)) + 'K'
    else:
        return str(round(inpt,2)) 