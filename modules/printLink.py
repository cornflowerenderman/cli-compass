def getFancyLink(text, target):
    return f"\u001b]8;;{target}\u001b\\{text}\u001b]8;;\u001b\\"

def printFancyLink(text, target):
    print(f"\u001b]8;;{target}\u001b\\{text}\u001b]8;;\u001b\\",end='')

