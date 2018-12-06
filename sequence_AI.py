from tkinter import *
from sequence import *
import time

# AI Class
class AI(object):

    # AI properties 
    def __init__(self):
        self.computerID = "4"

    # Getter for computer ID
    def getComputerID(self):
        return self.computerID
    
    # Finds the postions for all the cards in the computers hand
    def findCardLoc(self, computerDeck, cardBoard):
        allCardLoc = [(0, 0), (0, 9), (9, 9), (9, 0)]
        amtCards = 6
        for cardInd in range(amtCards):
            card = computerDeck.getCard(cardInd)
            cardLocs = cardBoard.locateCard(card)
            allCardLoc.extend(cardLocs)
        return allCardLoc

    # Removes positions that are already filled from card locations
    def removeInvalidPositions(self, cardLocations, pBoard):
        for i in range(len(cardLocations) - 1, -1, -1):
            if(pBoard.getPlayer(cardLocations[i][0], \
                                cardLocations[i][1]) != "0"):
                cardLocations.pop(i)
        return cardLocations

    # Finds the postions of all pieces a of computer
    def findPiecesLoc(self, pBoard):
        positions = []
        for row in range(pBoard.amtRows):
            for col in range(pBoard.amtCols):
                if(pBoard.getPlayer(row, col) == self.computerID):
                    positions.append((row, col))
        return positions

    # Finds the position for all pieces that are not computers
    def findOthersLoc(self, pBoard):
        positions = []
        for row in range(pBoard.amtRows):
            for col in range(pBoard.amtCols):
                if(pBoard.getPlayer(row, col) != self.computerID and \
                   pBoard.getPlayer(row, col) != "0"):
                    positions.append((row, col))
        return positions

    # Algorithm that determines best AI move
    def bestMove(self, computerDeck, pBoard, cardBoard):
        bestPos = (-1, -1)
        # Action if computer has two-eyed jack
        if(computerDeck.hasTwoEyedJack()):
            bestPos = self.playTwoEyedJack(pBoard)
        # Action if computer has one-eyed jack
        elif(computerDeck.hasOneEyedJack()):
            bestPos = self.playOneEyedJack(pBoard)
        # Computer plays normal move
        else:
            bestPos = self.playRegularPiece(computerDeck, pBoard, cardBoard)
        return bestPos

    # Action for playing a non special card 
    def playRegularPiece(self, computerDeck, pBoard, cardBoard):
        bestPos = (-1, -1)
        cardLocations = self.findCardLoc(computerDeck, cardBoard)
        cardLocations = self.removeInvalidPositions(cardLocations, pBoard)
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1)]
        # Max pieces from all cards
        bestPosMax = 0
        for cardLoc in cardLocations:
            row, col = cardLoc
            # Max pieces from every possible direction of a card
            maxDirPieces = 0
            for dirr in directions:
                # Max arrangement for a single direction 
                maxArrangement = 0
                for index in range(5):
                    tempRow = row + (-1)*(index * dirr[0])
                    tempCol = col + (-1)*(index * dirr[1])
                    # Amount of pieces for each arrangement
                    arrangementValue = self.calcAmtPieces(tempRow, tempCol, \
                                                          dirr, pBoard)
                    if(arrangementValue > maxArrangement):
                        maxArrangement = arrangementValue
                if(maxArrangement > maxDirPieces):
                    maxDirPieces = maxArrangement
            if(maxDirPieces > bestPosMax):
                bestPosMax = maxDirPieces
                bestPos = (row, col)
        if(bestPosMax == 0):
           card = computerDeck.getCard(0)
           cardLocs = cardBoard.locateCard(card)
           bestPos = cardLocs[0]
        return bestPos

    # Action for playing a two-eyed jack
    def playTwoEyedJack(self, pBoard):
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        while(pBoard.getPlayer(row, col) != "0"):
            row = random.randint(0, 9)
            col = random.randint(0, 9)
        return (row, col)      

    # Action for playing one-eyed jack
    def playOneEyedJack(self, pBoard):
        # Finds players pieces
        piecesLocations = self.findOthersLoc(pBoard)
        # Removes a random piece 
        amtPieces = len(piecesLocations)
        randInd = random.randint(0, amtPieces - 1)
        pos = piecesLocations[randInd]
        pBoard.setPlayer(pos[0], pos[1], "0")
        return (-1, -1)
        
    # Calculates the amount of pieces in a sequence of 5 for every direction
    def calcAmtPieces(self, row, col, dirr, pBoard):
        if(dirr == (-1, -1)):
            return self.calcDiagTL(pBoard, row, col)
        elif(dirr == (-1, 0)):
            return self.calcVertU(pBoard, row, col)
        elif(dirr == (-1, 1)):
            return self.calcDiagTR(pBoard, row, col)
        elif(dirr == (0, -1)):
            return self.calcHorizL(pBoard, row, col)
        elif(dirr == (0, 1)):
            return self.calcHorizR(pBoard, row, col)
        elif(dirr == (1, -1)):
            return self.calcDiagBL(pBoard, row, col)
        elif(dirr == (1, 0)):
            return self.calcVertD(pBoard, row, col)
        else:
            return self.calcDiagBR(pBoard, row, col)
       
    # Checks if passed row and column are within board confinements            
    def isInBounds(self, row, col, pBoard):
        return (0 <= row < PieceBoard.amtRows and 0 <= col < PieceBoard.amtCols)

    # Calculates the amount of computer pieces in rightwards horizontal sequence
    def calcHorizR(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row, col, pBoard) and \
               self.isInBounds(row, col + dis, pBoard)):
                if(pBoard.getPlayer(row, col + dis) == self.computerID):
                    total += 1
            else:
                return 0
        return total

    # Calculates the amount of computer pieces in leftwards horizontal sequence
    def calcHorizL(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row, col - dis, pBoard)):
                if(pBoard.getPlayer(row, col - dis) == self.computerID):
                    total += 1
            else:
                return 0
        return total

    # Calculates the amount of computer pieces in downwards vertical sequence
    def calcVertD(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row + dis, col, pBoard)):
                if(pBoard.getPlayer(row + dis, col) == self.computerID):
                    total += 1
            else:
                return 0
        return total

    # Calculates the amount of computer pieces in upwards vertical sequence
    def calcVertU(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row - dis, col, pBoard)):
                if(pBoard.getPlayer(row - dis, col) == self.computerID):
                    total += 1
            else:
                return 0
        return total

    # Calculates the amount of computer pieces in bottom right to top left
    # diagonal sequence
    def calcDiagTL(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row - dis, col - dis, pBoard)):
                if(pBoard.getPlayer(row - dis, col - dis) == self.computerID):
                    total += 1
            else:
                return 0
        return total
    
    # Calculates the amount of computer pieces in bottom left to top right
    # diagonal sequence
    def calcDiagTR(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row - dis, col + dis, pBoard)):
                if(pBoard.getPlayer(row - dis, col + dis) == self.computerID):
                    total += 1
            else:
                return 0
        return total

    # Calculates the amount of computer pieces in top right to bottom left
    # diagonal sequence
    def calcDiagBL(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row + dis, col - dis, pBoard)):
                if(pBoard.getPlayer(row + dis, col - dis) == self.computerID):
                    total += 1
            else:
                return 0
        return total

    # Calculates the amount of computer pieces in top left to bottom right
    # diagonal sequence
    def calcDiagBR(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row + dis, col + dis, pBoard)):
                if(pBoard.getPlayer(row + dis, col + dis) == self.computerID):
                    total += 1
            else:
                return 0
        return total

# Code acquired from CMU 15-112: Fundamentals of Programming and Computer
# Science Class Notes: Animation Part 2: Time-Based Animations in Tkinter
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# Data setup for AI
def init(data):
    # Data for 2 decks
    data.d1 = Deck()
    data.d2 = Deck()
    # Data for populated board of all the cards
    data.cardBoard = CardBoard()
    data.cardBoard.cardFillBoard()
    # Data for AI instance
    data.computer = AI()
    data.computerCards = PlayerDeck(data.d1, data.d2)
    # Data for players hand
    data.playerCards = PlayerDeck(data.d1, data.d2)
    # Data for boolean statements 
    data.computerTurn = False
    data.gameOver = False
    data.playedTurn = False
    data.receivedCard = False
    data.computerWon = False
    # Data for holding player numbers
    data.playerID = "1"
    # Data for creation of piece board
    data.pBoard = PieceBoard()
    # Data for drawing purposes
    data.margin = 200
    # Data for all buttons created
    data.getCardBtn = NewCardBtn(data.width - 2 * Card.cardWidth, \
                                 data.height // 2 - data.margin // 2)
    data.endTurnBtn = Btn("red", "End Turn", data.width - data.margin, \
                                  data.height - data.margin)
    
# When a player clicks one of the cards in their hand it checks if the
# positions in the board are filled and if they are it replaces the card
# from the players hand
def playerClickedHandCardEvent(data, xCoord, yCoord):
    # get the card
    cardInd = data.playerCards.clickedHandCard(xCoord, yCoord)
    card = data.playerCards.getCard(cardInd)
    # Find location of card in CardBoard
    positions = data.cardBoard.locateCard(card)
    loc1 = positions[0]
    loc1R = loc1[0]
    loc1C = loc1[1]
    loc2 = positions[1]
    loc2R = loc2[0]
    loc2C = loc2[1]
    # Check if positions in piece board are filled
    if(len(positions) != 0 and \
       data.pBoard.getPlayer(loc1R, loc1C) != "0" and\
       data.pBoard.getPlayer(loc2R, loc2C) != "0"):
        # Remove Card from hand
        data.playerCards.removeClickedHandCard(card)
        # Give player a new card
        data.getCardBtn.buttonAction(data.playerCards, data.d1, data.d2)

# When a player clicks a corner piece we put their piece down and do not
# let them make more moves not geta a new card
def playerPlayedCornerPiece(data, row, col):
    data.playedTurn = True
    data.receivedCard = True
    data.pBoard.fillPosInPieceBoard(row, col, data.playerID)

# When a player makes a move, we remove the card they used from their hand
# and put the piece down on the board
def playerPlayedPiece(data, row, col):
    data.playedTurn = True
    data.playerCards.removeCard(data.cardBoard.getCard(row, col), "two")
    data.pBoard.fillPosInPieceBoard(row, col, data.playerID)

# When a player removes another players piece, we remove the card they used
# from their hand and put the piece down on the board
def playerRemovedPiece(data, row, col):
    data.playedTurn = True
    data.playerCards.removeCard(data.cardBoard.getCard(row, col), "one")
    data.pBoard.fillPosInPieceBoard(row, col, "0")

# Mouse pressed event
def mousePressed(event, data):
    row, col = data.pBoard.convertCoordToPos(event.x, event.y)
    # Checks if a player clicked a card in their deck (attempting)
    # to replace a card with no available positions.
    if(data.playerCards.clickedHandCard(event.x, event.y) > 0):
        playerClickedHandCardEvent(data, event.x, event.y)
    # Checks if the player has not played their turn yet
    elif(not data.playedTurn):
        # Checks if a player played a piece in a corner position
        if(data.pBoard.onPieceBoard(row, col) and\
           data.pBoard.isValidPos(row, col) and\
           data.pBoard.isCornerPiece(row, col)):
            playerPlayedCornerPiece(data, row, col)
            if(data.pBoard.winningBoard(0, 0)):
                data.gameOver = True
        # Checks if a player played a piece in a non-corner position
        elif(data.pBoard.onPieceBoard(row, col) and\
           data.pBoard.isValidPos(row, col) and\
           (data.playerCards.hasCard(data.cardBoard.getCard(row, col)) or\
            data.playerCards.hasTwoEyedJack())):
            playerPlayedPiece(data, row, col)
            if(data.pBoard.winningBoard(0, 0)):
                data.gameOver = True
        # Checks if a player tried to remove someone else's piece
        elif(data.pBoard.onPieceBoard(row, col) and\
             not data.pBoard.isValidPos(row, col) and\
             data.playerCards.hasOneEyedJack() and\
             data.playerID != data.pBoard.getPlayer(row, col)):
            playerRemovedPiece(data, row, col)
    # Checks if a player wants to get a new card after playing a turn
    elif(data.getCardBtn.buttonClicked(event.x, event.y) and \
         not data.receivedCard):
        data.getCardBtn.buttonAction(data.playerCards, data.d1, data.d2)
        data.receivedCard = True
    # Checks if a player wants to end their turn
    elif(data.endTurnBtn.buttonClicked(event.x, event.y)):
        data.playedTurn = False
        data.receivedCard = False
        data.computerTurn = True
        
# Key pressed event
def keyPressed(event, data):
    pass

# Gives computer a card
def giveCard(computerCards, card):
    tempHand = computerCards.getCards()
    tempHand.append(card)
    return tempHand

# Replaces cards from computer hand which have pieces on both pieces 
def replaceCards(computerCards, cardBoard, pBoard):
    for cardInd in range(len(computerCards.getCards())):
        positions = cardBoard.locateCard(computerCards.getCard(cardInd))
        if(len(positions) > 0):
            pos1 = positions[0]
            pos2 = positions[1]
            if(pBoard.getPlayer(pos1[0], pos1[1]) != "0" and \
               pBoard.getPlayer(pos2[0], pos2[1]) != "0"):
                computerCards.removeClickedHandCard(\
                    computerCards.getCard(cardInd))
                randDeck = random.randint(1, 2)
                if(randDeck == 1):
                    card = data.d1.getRandomCard()
                else:
                    card = data.d2.getRandomCard()
                giveCard(data.computerCards, card)

# Makes move for computer
def makeTurn(data):
    # Gets position for best move
    pos = data.computer.bestMove(data.computerCards, data.pBoard, \
                                     data.cardBoard)
    playedCard = data.cardBoard.getCard(pos[0], pos[1])
    print(playedCard)
    if(pos != (-1, -1)):
        # Places piece on board
        data.pBoard.setPlayer(pos[0], pos[1], data.computer.getComputerID())
        # Removes played card
        data.computerCards.removeCard(playedCard, "two")
    else:
        # Removes played card
        data.computerCards.removeCard(playedCard, "one")
    corners = {(0, 0), (0, 9), (9, 9), (9, 0)}
    if(pos not in corners):
        # Gives random card from random card
        randDeck = random.randint(1, 2)
        if(randDeck == 1):
            card = data.d1.getRandomCard()
        else:
            card = data.d2.getRandomCard()
        giveCard(data.computerCards, card)
    #print(data.computerCards.getCards())
    # Replaces any cards that need to be replaced
    replaceCards(data.computerCards, data.cardBoard, data.pBoard)
    # Ends computer turn 
    data.computerTurn = False

# Timer fired event
def timerFired(data):
    # Makes computer move
    if(data.computerTurn):
        time.sleep(3)
        makeTurn(data)
        if(data.pBoard.winningBoard(0, 0)):
            data.gameOver = True
            data.computerWon = True

# Draws winner screen
def drawWinnerScreen(canvas, data):
    if(data.computerWon):
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "purple")
        canvas.create_text(data.width // 2, data.height // 2, \
                           text = "Computer Won.", font = "Times 64")
    else:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "purple")
        canvas.create_text(data.width // 2, data.height // 2, \
                           text = "Player Won!", font = "Times 64")

def displayTurn(canvas, data):
    if(data.computerTurn):
        canvas.create_text(data.width - data.margin, data.margin // 2, \
                           text = "Computer Turn", font = "Times 32", \
                           fill = "orange")
    else:
        canvas.create_text(data.width - data.margin, data.margin // 2, \
                           text = "Your Turn", font = "Times 32", \
                           fill = "orange")
# Redraw all event
def redrawAll(canvas, data):
    if(data.gameOver):
        drawWinnerScreen(canvas, data)
    else:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "#1c263d")
        displayTurn(canvas, data)
        data.cardBoard.drawBoard(canvas)
        data.pBoard.drawPieces(canvas)
        data.playerCards.drawDeck(canvas)
        data.getCardBtn.drawBtn(canvas)
        data.endTurnBtn.drawBtn(canvas)
        

####################################
# use the run function as-is
####################################

# Code acquired from CMU 15-112: Fundamentals of Programming and Computer
# Science Class Notes: Animation Part 2: Time-Based Animations in Tkinter
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

def runTempGame(width=1400, height=810):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = Toplevel()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    init(data)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# Lines of code: 515
