# Initialize the arrays
taglist = []

tagarray=[
     0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0
]

poparray=[
     0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0
]

movearray=[
     0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0
]


def detect_tags():
    pass


def decide_pops(tags):
    i = 0
    for num in len(tagarray):
        if tagarray(i)
            poparray[i] = 1
        else:
            poparray[i] = 0


def movedecider(type):
    if type == "dumb":
        pass
    elif type == "traveler":
        pass
    else:
        print("Major error! Make sure to specify the movement tactic for 'movedecider', either 'dumb' or 'traveler'")
