import random
import time

choose = input("Input export style code")
f = open("gofish.txt", "w")

def nrint(output):
    print(output)
    if choose == "Y" or choose == "Y/":
        print(output, file=f)

def l_nrint(output):
    if choose == "Y":
        print(output, file=f)
    elif choose != "Y/" and choose != "/":
        print(output)

# game datasets

deck = ['A','2','3','4','5','6','7','8','9','10','J','Q','K','A','2','3','4','5','6','7','8','9','10','J','Q','K','A','2','3','4','5','6','7','8','9','10','J','Q','K','A','2','3','4','5','6','7','8','9','10','J','Q','K']
p1 = [] # player 1's deck
p2 = [] # player 2's deck
calledThisTurn = [] # tracker to prevent repetitive calling of ranks
player = 1 # player turn tracker
score = [0, 0] # score in a round tracker
winCount = [0, 0] # win tracker for win rate
gameNo = 0 # game number count for display
turnNo = 0 # turn number count for display
repetitioncount = 0 # input repetitions

# referral datasets
playingStyle1 = "" # input style for player 1
playingStyle2 = "" # input style for player 2
playingStyleLibrary = ['0','1','11','2','3','4','24']
values = {} # dictionary to check for count of cards in a certain rank in player's hand
tempCount = 0 # used to check for highest number of cards in one rank for playing style A
### can be reused for playing style Aa AND Ca, if wanted
tempArray = [] # memory for playing style B
tempap1 = [] # memory of called cards for player 1 for playing style B & sequence checker for style D
tempap2 = [] # above for player 2
tempap12 = [] # sequence checker for style BD
tempap22 = [] # above for player 2
tempp1 = "" # used to check for player 1's repeated card to call for playing style C
tempp2 = "" # above for player 2

#personality decisions
while playingStyle1 not in playingStyleLibrary:
    playingStyle1 = input("Input personality 1 :)") # input 0, 1, 11, 2, 3, 31, 32 or 33

while playingStyle2 not in playingStyleLibrary:
    playingStyle2 = input("Input personality 2 :)") # input 0, 1, 11, 2, 3, 31, 32 or 33

# repetition amount
while not repetitioncount > 0:
    try:
        repetitioncount = 100000# int(input("How many repetitions would you like?"))
        if repetitioncount > 1000000 and choose != "Y/" and choose != "/":
            print("Repetitions while text is not cut is limited to 1,000,000.")
            repetitioncount = 0
    except ValueError:
        pass

# GAME FUNCTION DEFINITIONS --------------------------------------------------------------------------------------

def shuffle(array): 
    random.shuffle(array)

def draw(hand, number):
    if len(deck) >= number:
        for i in range(number):
            hand.append(deck.pop(0))
    elif len(deck) < number:
        for i in range(len(deck)):
            hand.append(deck.pop(0))

def sort(array):
    array.sort()

def fours(array): #boolean, after which use deletionPlan()
    values.clear()
    for i in range(len(array)):
        if array[i] not in list(values.keys()):
            values[array[i]] = 1
        else:
            values[array[i]] += 1
    for j in values:
        if values[j] == 4:
            return True
    return False

def deletionPlanFours(array):
    for j in values:
        if values[j] == 4:
            for k in range(4):
                array.remove(j)
            if j in tempap1: # only for style B
                tempap1.remove(j)
            if j in tempap2: # only for style B
                tempap2.remove(j)
            break
    if array == [] and deck != []:
        draw(array, 7) #draw 7 cards if deletionPlan() sets card in hand to 0
        l_nrint(f"New cards have been drawn: {array}")

def deletionPlan(array):
    if array == [] and deck != []:
        draw(array, 7) #draw 7 cards if deletionPlan() sets card in hand to 0
        l_nrint(f"New cards have been drawn: {array}")

def checkForMatch(string, array): # check if card called for is present in opponent's hand
    if string in array:
        return True
    else:
        return False

def transfer(string, arrayGiving, arrayReceiving): # if checkForMatch is true, transfer cards to opponent
    arrayReceiving.extend([item for item in arrayGiving if item == string])
    arrayGiving[:] = [item for item in arrayGiving if item != string]

# STYLE CHOICE AND DEFINITIONS -----------------------------------------------------------------------------------

def choice(style, array, tempArray, tempArray2, temp): # style = playingStyle1/2
    if style == '0':
        return styleRandom(array)
    elif style == '1':
        return styleA(array)
    elif style == '11':
        return styleAa(array)
    elif style == '2':
        return styleB(array, tempArray)
    elif style == '3':
        return styleC(array, temp)
    elif style == '4':
        return styleD(array, tempArray)
    elif style == '24':
        return styleBD(array, tempArray, tempArray2)

##style definitions
def styleRandom(array): # output a rank (string) to call
    tempArray = list(set(array))
    if [item for item in tempArray if item not in calledThisTurn] == []:
        return random.choice(tempArray)
    else:
        return random.choice([item for item in tempArray if item not in calledThisTurn])
    
def styleA(array): # style A: call for card you have more of
    values.clear()
    tempArray = []
    tempCount = 3
    for i in range(len(array)): # form dictionary of how many copies of each rank
        if array[i] in calledThisTurn:
            pass
        elif array[i] not in list(values.keys()):
            values[array[i]] = 1
        else:
            values[array[i]] += 1
    if values:
        for j in values: # finds all ranks with highest counts and randomises one
            if values[j] == tempCount:
                tempArray.append(j)
            elif values[j] < tempCount:
                tempCount = values[j]
                tempArray[:] = []
                tempArray.append(j)
    else:
        tempArray = list(set(array))
    return random.choice(tempArray)

def styleAa(array): # call for cards with different n at different times # breaks midway
    values.clear()
    tempArray = []
    if len(deck) < 19: # check for number of cards in deck, set n to call based on this
        tempCount = 3
    elif len(deck) < 27:
        tempCount = 2
    else:
        tempCount = 1
#### repeated code in Ca
    for i in range(len(array)): # form dictionary of how many copies of each rank
        if array[i] in calledThisTurn:
            pass
        elif array[i] not in list(values.keys()):
            values[array[i]] = 1
        else:
            values[array[i]] += 1
    if values:
        for j in values: # finds all ranks with specific count and randomises one
            if values[j] == tempCount:
                tempArray.append(j)
        while not tempArray:
            for i in range(3):
                tempCount = i + 1
                for j in values: # finds all ranks with highest counts and randomises one
                    if values[j] == tempCount:
                        tempArray.append(j)
                if tempArray:
                    break
    else:
        tempArray = list(set(array))
    return random.choice(tempArray)

def styleB(array, temp): # style B: memory of ranks called beforehand
    tempArray = list(set(array)) # list of unique ranks (what can be called for)
    if [item for item in tempArray if item in temp] != []:
        return random.choice([item for item in tempArray if item in temp])
    elif [item for item in tempArray if item in temp] == [] and [item for item in tempArray if item not in calledThisTurn] == []:
        return random.choice(tempArray)
    else:
        return random.choice([item for item in tempArray if item not in calledThisTurn])
    # check if any matches in tempArray and opponent called before
    # if so, randomise one to call for, and remove it from the list
    # if not, go random!!!

def styleC(array, temp): # style C: repeated calling
    if temp == "":
        tempArray = list(set(array))
        random.choice(tempArray)
        return random.choice(tempArray)
    elif temp in array and calledThisTurn == []:
        return temp
    else:
        tempArray = list(set(array))
        if [item for item in tempArray if item not in calledThisTurn] == []:
            return random.choice(tempArray)
        else:
            return random.choice([item for item in tempArray if item not in calledThisTurn])
    #check if card which you are calling is present (create a new variable for memory storage)
    #if it is, keep calling
    #if it is not, randomise a new rank (with parameters?) to call

def styleD(array, temp):
    tempArray = list(set(array))
    if not set(tempArray).issubset(set(temp)):
        for i in tempArray:
            if i not in temp:
                return i
    else:
        return tempArray[0]
    
def styleBD(array, temp1, temp2):
    tempArray = list(set(array)) # list of unique ranks (what can be called for)
    if [item for item in tempArray if item in temp1] != []:
        return random.choice([item for item in tempArray if item in temp1])
    else:
        if not set(tempArray).issubset(set(temp2)):
            for i in tempArray:
                if i not in temp2 and i not in calledThisTurn:
                        return i
        else:
            return tempArray[0]

# GAME SIMULATION AND PROGRESS TRACKER -----------------------------------------------------------------------------

for i in range(repetitioncount):
    gameNo += 1
    l_nrint(f"Game {gameNo}")
    if (choose == "Y" or choose == "Y/" or choose == "/") and gameNo != 1 :            ## progress bar
        print(f"Progress: On Game {gameNo}... Win rate: {winCount[0]/(gameNo-1)}", end='\r', flush=True)
    l_nrint(10 * "-")
    player = 1

    deck = ['A','2','3','4','5','6','7','8','9','10','J','Q','K','A','2','3','4','5','6','7','8','9','10','J','Q','K','A','2','3','4','5','6','7','8','9','10','J','Q','K','A','2','3','4','5','6','7','8','9','10','J','Q','K']
    shuffle(deck)
    draw(p1, 7)
    draw(p2, 7)
    sort(p1)
    sort(p2)

    if fours(p1):
        deletionPlanFours(p1)
        score[0] += 1
    if fours(p2):
        deletionPlanFours(p2)
        score[1] += 1

    tempp1 = ""
    tempp2 = ""
    tempap1 = []
    tempap2 = []
    tempap12 = []
    tempap22 = []

    while deck or p1 or p2:     ## actual
    #for i in range(20):         ## testing
        if player == 1:
            turnNo += 1
            l_nrint(f"Turn {turnNo}")

            l_nrint(f"P1: {p1}, P2: {p2}, P1 turn. Score: {score}")
            while True:
                calledThisTurn.append(choice(playingStyle1, p1, tempap1, tempap12, tempp1)) # calledThisTurn[-1] is rank last called for
                if calledThisTurn[-1] not in tempap2 and playingStyle2[0] == "2": # for style B only
                    tempap2.append(calledThisTurn[-1])
                if calledThisTurn[-1] in tempap1 and playingStyle1[0] == "2":
                    tempap1.remove(calledThisTurn[-1])
                tempp1 = calledThisTurn[0] # for style C only
                if playingStyle1 == "4": # for style D only
                    if calledThisTurn[-1] not in tempap1:
                        tempap1.append(calledThisTurn[-1])
                    else:
                        tempap1 = [calledThisTurn[-1]]
                if playingStyle1 == "24": # for style BD only
                    if calledThisTurn[-1] not in tempap12:
                        tempap12.append(calledThisTurn[-1])
                    else:
                        tempap12 = [calledThisTurn[-1]]
                if checkForMatch(calledThisTurn[-1], p2):
                    l_nrint(f"P1 asks P2 for a {calledThisTurn[-1]}. P2 has a {calledThisTurn[-1]}!")
                    transfer(calledThisTurn[-1], p2, p1)
                    deletionPlan(p2)
                    while fours(p1):
                        deletionPlanFours(p1)
                        score[0] += 1
                    while fours(p2):
                        deletionPlanFours(p2)
                        score[1] += 1
                    if not (deck or p1 or p2):
                        break
                else:
                    draw(p1, 1)
                    if p1[-1] == calledThisTurn[-1]:
                        l_nrint(f"P1 asks P2 for a {calledThisTurn[-1]}. P2 tells P1 to Go Fish! P1 draws a {calledThisTurn[-1]} and can ask again!")
                        while fours(p1):
                            deletionPlanFours(p1)
                            score[0] += 1
                        if not (deck or p1 or p2):
                            break
                    else:
                        l_nrint(f"P1 asks P2 for a {calledThisTurn[-1]}. P2 tells P1 to Go Fish! P1 draws a {p1[-1]}.")
                        while fours(p1):
                            deletionPlanFours(p1)
                            score[0] += 1
                        calledThisTurn[:] = []
                        break
                if not (deck or p1 or p2):
                    break
            player = 2
        elif player == 2:
            turnNo += 1
            l_nrint(f"Turn {turnNo}")

            l_nrint(f"P1: {p1}, P2: {p2}, P2 turn. Score: {score}")
            while True:
                calledThisTurn.append(choice(playingStyle2, p2, tempap2, tempap22, tempp2)) # calledThisTurn[-1] is rank last called for
                if calledThisTurn[-1] not in tempap1 and playingStyle1[0] == "2": # for style B only
                    tempap1.append(calledThisTurn[-1])
                if calledThisTurn[-1] in tempap2 and playingStyle2[0] == "2":
                    tempap2.remove(calledThisTurn[-1])
                tempp2 = calledThisTurn[0] # for style C only
                if playingStyle2 == "4": # for style D only
                    if calledThisTurn[-1] not in tempap2:
                        tempap2.append(calledThisTurn[-1])
                    else:
                        tempap2 = [calledThisTurn[-1]]
                if playingStyle2 == "24": # for style BD only
                    if calledThisTurn[-1] not in tempap22:
                        tempap22.append(calledThisTurn[-1])
                    else:
                        tempap22 = [calledThisTurn[-1]]
                if checkForMatch(calledThisTurn[-1], p1):
                    l_nrint(f"P2 asks P1 for a {calledThisTurn[-1]}. P1 has a {calledThisTurn[-1]}!")
                    transfer(calledThisTurn[-1], p1, p2)
                    deletionPlan(p1)
                    while fours(p2):
                        deletionPlanFours(p2)
                        score[1] += 1
                    while fours(p1):
                        deletionPlanFours(p1)
                        score[0] += 1
                    if not (deck or p1 or p2):
                        break
                else:
                    draw(p2, 1)
                    if p2[-1] == calledThisTurn[-1]:
                        l_nrint(f"P2 asks P1 for a {calledThisTurn[-1]}. P1 tells P2 to Go Fish! P2 draws a {calledThisTurn[-1]} and can ask again!")
                        while fours(p2):
                            deletionPlanFours(p2)
                            score[1] += 1
                        if not (deck or p1 or p2):
                            break
                    else:
                        l_nrint(f"P2 asks P1 for a {calledThisTurn[-1]}. P1 tells P2 to Go Fish! P2 draws a {p2[-1]}.")
                        while fours(p2):
                            deletionPlanFours(p2)
                            score[1] += 1
                        calledThisTurn[:] = []
                        break
            player = 1
        sort(p1)
        sort(p2)
        l_nrint("")

    if score[0] > score[1]:
        l_nrint(f"P1 has won {score[0]} to {score[1]}!")
        winCount[0] += 1
    elif score[0] < score[1]:
        l_nrint(f"P2 has won {score[1]} to {score[0]}!")
        winCount[1] += 1
    else:
        l_nrint("how did you tie theres 13 sets")

    score[:] = [0, 0]
    turnNo = 0
    l_nrint(30 * "-")
    # time.sleep(0.01) # for slow analysis

nrint(f"P1 has won {winCount[0]} times out of {repetitioncount}, win rate: {winCount[0]/repetitioncount}")
nrint(f"P2 has won {winCount[1]} times out of {repetitioncount}, win rate: {winCount[1]/repetitioncount}")

##### known issues #######################################################################

# 4 is untested

##### usage notes ########################################################################

# input 1: data output method, input 2: style for p1, input 3: style for p2, input 4: repetitions
# data output is separated into Y, / and [no input]
### Y --> in txt file, / --> only output final winrate, [no input] --> output in console
# style descs are below under ## planning ##

# nrint --> print in console and can print in notepad if indicated
# l_nrint --> may not print if excess info not wanted

# runtime
# Y, 0, 0, 10000 takes 3 seconds
# Y, 0, 0, 100000 takes 30 seconds
# Y, 0, 0, 1000000 takes a few minutes
# other styles take slightly longer
# [no input] is slower than Y

# against 0, 1 & 3 seem to be worse styles
# 2 is definitely the best
# 4 is untested

##### planning ###########################################################################

# n = 4 - count of rank in player's hand

# "personalities" design

# style A: call for card you have more of
# - count number of each rank in player's hand
# - generate list of ranks, randomise which one to call
### tweak idea (call it style A1): call at the right time
### - based on ratio of number of cards left in deck to n at start of game
### - generate list of ranks, checking for specific n, randomise which one to call

# style B: memory of ranks called beforehand
# - store a memory bank (array) of ranks called beforehand
# - check if anything in the memory bank matches with a card the player has
# - call for that card
# - if not, randomise

# style C: repeated calling
# - randomise a rank and ask for it until its completed
# - when completed, randomise again

# style D: call in specific order
# - using sorted array, pick the closest uncalled rank to the left of the array to call
# - when no more available, clear and start from front again

# gameplay flow
# - nrint hand (P1 [], P2 [])
# - generate rank to call (P1 asks for rank ??)
# - if P2 has rank, (P2 has a ??), P1 asks again, repeat [run fours(), use calledThisTurn to ensure no repeats unless necessary]
# - if P2 does not have rank, (P2 tells P1 to go fish!)
# - P1 draw() a card, if it matches, (P1 draws a ??!) then repeat from start, call for a different rank (use calledThisTurn to ensure no repeats unless necessary)
# - if it doesn't match, (P1 draws a ??.) [either way, run fours()]
# - if fours() is true, activate deletionPlan()
# - whenever player hand is empty (ergo array empty), run draw(array, 7)

# current console log configuration:
# Turn 1
# P1 [A, A, 2, 2, 3, 3, 4]; P2 [5, 5, 6, 6, 7, 7, 8]. Score: [0, 0]
# P1 asks for rank 3. P2 tells P1 to go fish! P1 draws a 3!
# P1 asks for rank 4, P2 tells P1 to go fish! P1 draws a 10.
# Turn 2
# P1 [A, A, 2, 2, 3, 3, 3, 4, 10]; P2 [5, 5, 6, 6, 7, 7, 8]. Score [0, 0]

# console log idea:
# Turn 1: P1 [A, A, 2, 2, 3, 3, 4]; P2 [5, 5, 6, 6, 7, 7, 8], P1 turn. Score [0, 0]
# failed call for 3, 3 drawn, failed call for 4, 10 drawn --> made by a doubly nested array tracking each rank as a variable
# Turn 2: P1 [A, A, 2, 2, 3, 3, 3, 4, 10]; P2 [5, 5, 6, 6, 7, 7, 8], P2 turn. Score [0, 0]

# additional data i could get just for fun:
# - bell curve of turn counts?
# - 