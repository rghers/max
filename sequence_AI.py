from sequence import *
import time

class AI(object):

    def __init__(self):
        self.computerID = "4"

    def getComputerID(self):
        return self.computerID

    def findCardLoc(self, computerDeck, cardBoard):
        allCardLoc = [(0, 0), (0, 9), (9, 9), (9, 0)]
        amtCards = 6
        for cardInd in range(amtCards):
            card = computerDeck.getCard(cardInd)
            cardLocs = cardBoard.locateCard(card)
            allCardLoc.extend(cardLocs)
        return allCardLoc
        

    def bestMove(self, computerDeck, pBoard, cardBoard):
        bestPos = (-1, -1)
        cardLocations = self.findCardLoc(computerDeck, cardBoard)
        # if comp has two eyed jack
        # if has one eyed jack and player about to win
        directions = [(-1, -1), (-1, 0), (-1, 1), \
                (0, -1), (0, 1), \
                (1, -1), (1, 0), (1, 1)]
        bestDirVal = 0
        for cardLoc in cardLocations:
            row = cardLoc[0]
            col = cardLoc[1]
            if(pBoard.getPlayer(row, col) != "0"):
                continue
            maxDirVal = 0
            for dirr in directions:
                dirVal = self.calcAmtPieces(row, col, dirr, pBoard)
                if(dirVal > maxDirVal):
                    maxDirVal = dirVal
            if(maxDirVal > bestDirVal):
                bestDirVal = maxDirVal
                bestPos = (row, col)
        if(bestDirVal == 0):
           card = computerDeck.getCard(0)
           cardLocs = cardBoard.locateCard(card)
           bestPos = cardLocs[0]
        return bestPos

    def calcAmtPieces(self, row, col, dirr, pBoard):
        if(dirr == (-1, -1)):
            return self.calcDiagBR(pBoard, row, col)
        elif(dirr == (-1, 0)):
            return self.calcVertU(pBoard, row, col)
        elif(dirr == (-1, 1)):
            return self.calcDiagBL(pBoard, row, col)
        elif(dirr == (0, -1)):
            return self.calcHorizL(pBoard, row, col)
        elif(dirr == (0, 1)):
            return self.calcHorizR(pBoard, row, col)
        elif(dirr == (1, -1)):
            return self.calcDiagTR(pBoard, row, col)
        elif(dirr == (1, 0)):
            return self.calcVertD(pBoard, row, col)
        else:
            return self.calcDiagTL(pBoard, row, col)
       
            
    def isInBounds(self, row, col, pBoard):
        return (0 <= row < PieceBoard.amtRows and 0 <= col < PieceBoard.amtCols)


    def calcHorizR(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row, col + dis, pBoard)):
                if(pBoard.getPlayer(row, col + dis) == self.computerID):
                    total += 1
            else:
                return 0
        return total

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

    def calcDiagTL(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row + dis, col + dis, pBoard)):
                if(pBoard.getPlayer(row + dis, col + dis) == self.computerID):
                    total += 1
            else:
                return 0
        return total

    def calcDiagTR(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row + dis, col - dis, pBoard)):
                if(pBoard.getPlayer(row + dis, col - dis) == self.computerID):
                    total += 1
            else:
                return 0
        return total

    def calcDiagBL(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row - dis, col - dis, pBoard)):
                if(pBoard.getPlayer(row - dis, col - dis) == self.computerID):
                    total += 1
            else:
                return 0
        return total

    def calcDiagBR(self, pBoard, row, col):
        amtComparisons = 5
        total = 0
        for dis in range(amtComparisons):
            if(self.isInBounds(row - dis, col + dis, pBoard)):
                if(pBoard.getPlayer(row - dis, col + dis) == self.computerID):
                    total += 1
            else:
                return 0
        return total

##    def bestMove(self, pBoard, playerID):
##        bestPos = (0, 0)
##        bestPosDirr = ""
##        maxCons = -1
##        for row in range(len(pBoard)):
##            for col in range(len(pBoard[0])):
##                if(pBoard.getPlayer(row, col) != playerID):
##                    rcStreak, dirr = 
##                    
##
##    def bestDirForRC(self, pBoard):
##        amtInHoriz = self.calcHoriz(row, col)
##        if(self.hasValidOpening(row, col, 0, 1)):                       
##        amtInVert = self.calcVert(row, col)
##        amtInDiag1 = self.calcDiag1(row, col)
##        amtInDiag2 = self.calcDiag2(row, col)
##        
##                    

##                
##

            
        
        


def init(data):
    data.computer = AI()
    data.d1 = Deck()
    data.d2 = Deck()
    data.cardBoard = CardBoard()
    data.cardBoard.cardFillBoard()
    data.playerCards = PlayerDeck(data.d1, data.d2)
    data.computerCards = PlayerDeck(data.d1, data.d2)
    data.computerTurn = False
    data.gameOver = False
    data.playedTurn = False
    data.receivedCard = False
    data.computerWon = False
    data.pBoard = PieceBoard()
    data.margin = 200
    data.getCardBtn = NewCardBtn(data.width - 2 * Card.cardWidth, \
                                 data.height // 2 - data.margin // 2)
    data.endTurnBtn = Btn("red", "End Turn", data.width - data.margin, \
                                  data.height - data.margin)
    


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

def playerPlayedCornerPiece(data, row, col):
    data.playedTurn = True
    data.receivedCard = True
    data.pBoard.fillPosInPieceBoard(row, col, data.playerID)

def playerPlayedPiece(data, row, col):
    data.playedTurn = True
    data.playerCards.removeCard(data.cardBoard.getCard(row, col), "two")
    data.pBoard.fillPosInPieceBoard(row, col, data.playerID)

def playerRemovedPiece(data, row, col):
    data.playedTurn = True
    data.playerCards.removeCard(data.cardBoard.getCard(row, col), "one")
    data.pBoard.fillPosInPieceBoard(row, col, "0")
    
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
        print(data.computerCards.getCards())


def keyPressed(event, data):
    pass

def giveCard(computerCards, card):
    tempHand = computerCards.getCards()
    tempHand.append(card)
    return tempHand

def replaceCards(computerCards, cardBoard, pBoard):
    for cardInd in range(len(computerCards.getCards())):
        positions = cardBoard.locateCard(computerCards.getCard(cardInd))
        if(len(positions) > 0):
            pos1 = positions[0]
            pos2 = positions[1]
            if(pBoard.getPlayer(pos1[0], pos1[1]) != "0" and \
               pBoard.getPlayer(pos2[0], pos2[1]) != "0"):
                computerCards.removeClickedHandCard(computerCards.getCard(cardInd))
                randDeck = random.randint(1, 2)
                if(randDeck == 1):
                    card = data.d1.getRandomCard()
                else:
                    card = data.d2.getRandomCard()
                giveCard(data.computerCards, card)
                

def makeTurn(data):
    pos = data.computer.bestMove(data.computerCards, data.pBoard, \
                                     data.cardBoard)
    data.pBoard.setPlayer(pos[0], pos[1], data.computer.getComputerID())
    playedCard = data.cardBoard.getCard(pos[0], pos[1])
    data.computerCards.removeCard(playedCard, "two")
    randDeck = random.randint(1, 2)
    if(randDeck == 1):
        card = data.d1.getRandomCard()
    else:
        card = data.d2.getRandomCard()
    giveCard(data.computerCards, card)
    replaceCards(data.computerCards)
    data.computerTurn = False
    
def timerFired(data):
    if(data.computerTurn):
        print("it is the computer turn")
        time.sleep(3)
        makeTurn(data)
        if(data.pBoard.winningBoard(0, 0)):
            data.gameOver = True
            data.computerWon = True

def drawWinnerScreen(canvas, data):
    if(data.computerWon):
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "purple")
        canvas.create_text(data.width // 2, data.height // 2, \
                           text = "Computer Won.", font = "Times 64")
    else:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "purple")
        canvas.create_text(data.width // 2, data.height // 2, \
                           text = "Player Won!", font = "Times 64")
        
def redrawAll(canvas, data):
    print("in redraw all of AI")
    if(data.gameOver):
        drawWinnerScreen(canvas, data)
       #canvas.create_rectangle(0, 0, data.width, data.height, fill = "red")
    
    else:
        print("in else of redraw all of AI")
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "#1c263d")
        #canvas.create_image(0, 0, anchor = NW, \
        #                    image = data.pokerTableImg)
        print("before draw board in AI")
        data.cardBoard.drawBoard(canvas)
        print("after draw board in AI")
        ## Temp State ##
        data.pBoard.drawPieces(canvas)
        print("after draw pieces in AI")
        ## END ## 
        data.playerCards.drawDeck(canvas)
        print("after draw deck in AI")
        data.getCardBtn.drawBtn(canvas)
        data.endTurnBtn.drawBtn(canvas)
        

####################################
# use the run function as-is
####################################

def runTempGame(playerID, width=1400, height=810):
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
    data.playerID = playerID
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = Tk()
    init(data)
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
#runTempGame("1")

