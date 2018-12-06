from tkinter import *
from PIL import Image, ImageTk, ImageOps
import random
import json

# Adapted from course notes of OOPy: Playing Card Demo
# https://www.cs.cmu.edu/~112/notes/notes-oop.html
# Card class
class Card(object):
    numberNames = [None, "Ace", "2", "3", "4", "5", "6", "7",
                   "8", "9", "10", "Jack", "Queen", "King"]
    suitNames = ["Clubs", "Diamonds", "Hearts", "Spades", "x"]
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3
    cardHeight = 71
    cardWidth = 96

    # Card properties
    def __init__(self, number = 2, suit = 4):
        # number is 1 for Ace, 2...10,
        #           11 for Jack, 12 for Queen, 13 for King
        # suit is 0 for Clubs, 1 for Diamonds,
        #         2 for Hearts, 3 for Spades
        self.number = number
        self.suit = suit
        # Card images acquired from CMU 15-112: Fundamentals of Programming and
        # Computer Science Class Notes: Animation Demos / Images Demo
        # https://www.cs.cmu.edu/~112/notes/notes-animations-demos.html

        # Code structure for images learned from Image module on PIL documentation
        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
        self.filename = "playing-card-gifs/%s%d.gif" % \
                        (Card.suitNames[self.suit][0].lower(),\
                         self.number)
        #print("the file name is: ",self.filename)
        self.img = Image.open(self.filename)
        self.img = self.img.resize((Card.cardWidth, Card.cardHeight))
        self.picture = ImageTk.PhotoImage(self.img)
        
    # String representation of Card
    def __repr__(self):
        return ("<%s of %s>" %
                (Card.numberNames[self.number],
                 Card.suitNames[self.suit]))
    
    def getHashables(self):
        return (self.number, self.suit) # return a tuple of hashables

    # Turns cards properties into a hashable item
    def __hash__(self):
        return hash(self.getHashables())

    # Getter for card number
    def getNumber(self):
        return self[0]

    # Getter for suit value
    def getSuit(self):
        return self[1]

    # Compares cards based on suit and value
    def __eq__(self, other):
        return (isinstance(other, Card) and
                (self.number == other.number) and
                (self.suit == other.suit))
    
    # Draws playing card 
    def drawPlayingCard(self, canvas, xPos, yPos):
        pic = self.picture
        canvas.create_image(xPos, yPos, image = pic)

# Deck class        
class Deck(object):

    # Deck properties
    def __init__(self):
        self.deck = self.createDeck()
        self.usedCards = set()

    # Creates a deck containing all non-special(jokers and back) cards
    def createDeck(self):
        cards = []
        for rank in range(len(Card.numberNames)):
            for suit in range(len(Card.suitNames) - 1):
                if(rank != 0):
                    card = Card(rank, suit)
                    cards.append(card)
        return cards

    # Gets a random card from this deck and ensures that card has not already
    # been picked
    def getRandomCard(self):
        randCardIndex = random.randint(0, 51)
        while(self.deck[randCardIndex] in self.usedCards):
            randCardIndex = random.randint(0, 51)
        self.usedCards.add(self.deck[randCardIndex])
        return self.deck[randCardIndex]

    # Shuffles the deck
    def shuffleDeck(self):
        random.shuffle(self.deck)

    # String representation of Deck
    def __repr__(self):
        return "Deck is: \n" + str(self.deck)

    
# Card Board Class
class CardBoard(object):
    amtRows = 10
    amtCols = 10
    # Matrix of tuples containing (value, suit) of cards
    board = [[(-1, -1), (10, 3), (12, 3), (13, 3), (1, 3), \
              (2, 1), (3, 1), (4, 1), (5, 1), (-1, -1)],
             [(9, 3), (10, 2), (9, 2), (8, 2), (7, 2), \
              (6, 2), (5, 2), (4, 2), (3, 2), (6, 1)],
             [(8, 3), (12, 2), (7, 1), (8, 1), (9, 1), \
              (10, 1), (12, 1), (13, 1), (2, 2), (7, 1)],
             [(7, 3), (13, 2), (6, 1), (2, 0), (1, 2), \
              (13, 2), (12, 2), (1, 1), (2, 3), (8, 1)],
             [(6, 3), (1, 2), (5, 1), (3, 0), (4, 2), \
              (3, 2), (10, 2), (1, 0), (3, 3), (9, 1)],
             [(5, 3), (2, 0), (4, 1), (4, 0), (5, 2), \
              (2, 2), (9, 2), (13, 0), (4, 3), (10, 1)],
             [(4, 3), (3, 0), (3, 1), (5, 0), (6, 2), \
              (7, 2), (8, 2), (12, 0), (5, 3), (12, 1)],
             [(3, 3), (4, 0), (2, 1), (6, 0), (7, 0), \
              (8, 0), (9, 0), (10, 0), (6, 3), (13, 1)],
             [(2, 3), (5, 0), (1, 3), (13, 3), (12, 3), \
              (10, 3), (9, 3), (8, 3), (7, 3), (1, 1)],
             [(-1, -1), (6, 0), (7, 0), (8, 0), (9, 0), \
              (10, 0), (12, 0), (13, 0), (1, 0), (-1, -1)]]
    seperationX = 70
    seperationY = 40

    # CardBoard properties 
    def __init__(self):
        self.board = CardBoard.board
        
    # Repopulates the board position with respective cards by accessing tuple
    # values
    def cardFillBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if (isinstance(self.board[row][col], tuple)):
                    if(self.board[row][col] == (-1, -1)):
                        self.board[row][col] = Card()
                    else:
                        c = self.getCard(row,col)
                        rank= Card.getNumber(c)
                        suit= Card.getSuit(c)                
                        myCard = Card(rank, suit)
                        self.board[row][col] = myCard
        
    # Finds the two row and column postions for passed card
    def locateCard(self, card):
        positions = []
        for row in range(CardBoard.amtRows):
            for col in range(CardBoard.amtCols):
                cardRC = self.board[row][col]
                if(cardRC == card):
                    positions.append((row, col))
        return positions

    # Draws the card board
    def drawBoard(self, canvas):
        for row in range(CardBoard.amtRows):
            for col in range(CardBoard.amtCols):
                card = self.getCard(row, col)
                card.drawPlayingCard(canvas, CardBoard.seperationX + \
                                     Card.cardWidth * col, \
                                     CardBoard.seperationY + \
                                     Card.cardHeight * row)

    # Prints the card board
    def printBoard(self):
        print(self.board)
                
    # Returns the card at a given row and column
    def getCard(self, row, col):
        return self.board[row][col]

# Player Deck Class
class PlayerDeck(object):

    # PlayerDeck properties
    def __init__(self, cardDeck1, cardDeck2):
        self.cardDeck1 = cardDeck1
        self.cardDeck2 = cardDeck2
        self.amtCards = 6
        self.playerCards = self.giveStaringCards(self.cardDeck1, \
                                                 self.cardDeck2)
        # Starting positions on Tkinter for the deck drawing 
        self.startingX = 125
        self.startingY = 775
        self.xChange = 150
        
    # Gives a player the initial 6 starting cards
    def giveStaringCards(self, cardDeck1, cardDeck2):
        tempHand = []
        for i in range(self.amtCards):
            if(i % 2 == 0):
                card = self.cardDeck1.getRandomCard()
            else:
                card = self.cardDeck2.getRandomCard()
            tempHand.append(card)
        return tempHand

    # Returns the cards in the players hand
    def getCards(self):
        return self.playerCards

    # Gets a specific card within the players hand
    def getCard(self, index):
        return self.playerCards[index]

    # Draws the players hand
    def drawDeck(self, canvas):
        x = self.startingX
        y = self.startingY
        for card in self.playerCards:
            card.drawPlayingCard(canvas, x, y)
            x += self.xChange
            
    # Checks if a player has a given card in their hand
    def hasCard(self, selectedCard):
        for card in self.playerCards:
            if(card == selectedCard):
                return True
        return False

    # Checks if the player has a two eyed jack (special card)
    def hasTwoEyedJack(self):
        s = {Card(11, 0), Card(11, 1)}
        for card in self.playerCards:
            if(card in s):
                return True
        return False
    
    # Checks if the player has a one eyed jack (special card)
    def hasOneEyedJack(self):
        s = {Card(11, 2), Card(11, 3)}
        for card in self.playerCards:
            if(card in s):
                return True
        return False

    # Removes a passed card from the players hand
    def removeCard(self, selectedCard, amtEyes):
        if(amtEyes == "two"):
            for cardInd in range(len(self.playerCards)):
                if(self.playerCards[cardInd] == selectedCard):
                    self.playerCards.pop(cardInd)
                    return
            for cardInd in range(len(self.playerCards)):
                s = {Card(11, 0), Card(11, 1)}
                if(self.playerCards[cardInd] in s):
                    self.playerCards.pop(cardInd)
                    return
        elif(amtEyes == "one"):
            for cardInd in range(len(self.playerCards)):
                s = {Card(11, 2), Card(11, 3)}
                if(self.playerCards[cardInd] in s):
                    self.playerCards.pop(cardInd)
                    return

    # Checks if the player clicked on of their cards on Tkinter window
    # and converts coordinate click to an index position within player hand
    def clickedHandCard(self, xCoord, yCoord):
        for cardInd in range(len(self.playerCards)):
            xPos = self.startingX + self.xChange * cardInd
            yPos = self.startingY
            if(xPos - Card.cardWidth // 2 <= xCoord <= xPos + \
               Card.cardWidth and yPos - Card.cardHeight // 2 <= \
               yCoord <= yPos + Card.cardHeight):
                return cardInd
        return -1

    # Removes the clicked card 
    def removeClickedHandCard(self, card):
        for cardInd in range(len(self.playerCards)):
            if(self.playerCards[cardInd] == card):
                self.playerCards.pop(cardInd)
                return

# PieceBoard Class
class PieceBoard(object):
    amtRows = 10
    amtCols = 10
    # Initial state of piece board is a matrix with no pieces
    board = [["0"] * CardBoard.amtCols for row in range(CardBoard.amtRows)]
    
    # Piece Board properties
    def __init__(self):
        self.board = PieceBoard.board

    # String representation of the piece board
    def __repr__(self):
        return str(self.board)

    # Converts a click in Tkinter to respective row and column positions
    def convertCoordToPos(self, xCoord, yCoord):
        topLeftX = CardBoard.seperationX - Card.cardWidth // 2
        topLeftY = CardBoard.seperationY - Card.cardHeight // 2
        x = xCoord - topLeftX
        y = yCoord - topLeftY
        return (y // Card.cardHeight, x // Card.cardWidth)

    # Checks if click is within piece board boundaries
    def onPieceBoard(self, row, col):
        return (0 <= row < PieceBoard.amtRows and \
                0 <= col < PieceBoard.amtCols)

    # Fills the clicked position with the player number that clicked it
    def fillPosInPieceBoard(self, row, col, playerNum):
        self.board[row][col] = playerNum

    # Checks if the clicked postion is empty
    def isValidPos(self, row, col):
        return self.board[row][col] == "0"

    # Prints the piece board
    def printBoard(self):
        print(self.board)

    # Recursively checks if a connection of 5 pieces exists, meaning a
    # player has won the game
    def winningBoard(self, row, col):
        if(row >= len(self.board)):
            return False
        elif(self.board[row][col] == "0"):
            newRow, newCol = self.findNextRC(row, col)
            return self.winningBoard(newRow, newCol)
        # Only need to check these directions since their counterparts are
        # already accounted for by the way the check moves from position
        # to postion
        elif(self.diag1Consecutive(row, col) or\
             self.diag2Consecutive(row, col) or \
             self.horizConsecutive(row, col) or\
             self.vertConsecutive(row, col)):
            return True
        else:
            newRow, newCol = self.findNextRC(row, col)
            return self.winningBoard(newRow, newCol)

    # Resets the piece board
    def resetBoard(self):
        self.board = [["0"] * CardBoard.amtCols for row in range(CardBoard.amtRows)]

    # Moves to the next position on the piece board
    def findNextRC(self, row, col):
        if(col + 1 == len(self.board[0])):
            return (row+1, 0)
        return (row, col+1)

    # Checks if the row and column values are within piece board limits
    def inBounds(self, row, col):
        return (0 <= row < len(self.board) and \
                0 <= col < len(self.board[0]))

    # Checks if the top left to bottom right diagonal has 5 consecutive pieces
    # from the same player
    def diag1Consecutive(self, row, col):
        totalCons = 4
        for i in range(totalCons):
            if(not self.inBounds(row + i + 1, col + i + 1)):
                return False
            elif(not self.board[row + i][col + i] == \
               self.board[row + i + 1][col + i + 1]):
                return False
        return True

    # Checks if the top left to bottom left diagonal has 5 consecutive pieces
    # from the same player
    def diag2Consecutive(self, row, col):
        totalCons = 4
        for i in range(totalCons):
            if(not self.inBounds(row + i + 1, col - i - 1)):
                return False
            elif(not self.board[row + i][col - i] == \
               self.board[row + i + 1][col - i - 1]):
                return False
        return True
    
    # Checks if the rightward horizontal has 5 consecutive pieces from the
    # same player
    def horizConsecutive(self, row, col):
        totalCons = 4
        for i in range(totalCons):
            if(not self.inBounds(row, col + i + 1)):
                return False
            elif(not self.board[row][col + i] == \
               self.board[row][col + i + 1]):
                return False
        return True

    # Checks if the downward vertical has 5 consecutive pieces from the
    # same player
    def vertConsecutive(self, row, col):
        totalCons = 4
        for i in range(totalCons):
            if(not self.inBounds(row + i + 1, col)):
                return False
            elif(not self.board[row + i][col] == \
               self.board[row + i + 1][col]):
                return False
        return True

    # Returns the player piece or indicates no piece at a passed postion 
    def getPlayer(self, row, col):
        return self.board[row][col]

    # Sets the player to given player at a passed position
    def setPlayer(self, row, col, player):
        self.board[row][col] = player

    # Checks if the passed postion is a corner position
    def isCornerPiece(self, row, col):
        if((row == 0 and col == 0) or \
           (row == 0 and col == PieceBoard.amtCols- 1) or \
           (row == PieceBoard.amtRows - 1 and col == PieceBoard.amtCols - 1) or\
           (row == PieceBoard.amtRows - 1 and col == 0)):
            return True
        return False
    
    # Draws the pieces on the board 
    def drawPieces(self, canvas):
        for row in range(PieceBoard.amtRows):
            for col in range(PieceBoard.amtCols):
                if(self.board[row][col] != "0"):
                    # Rectangle represents Piece and color represents player
                    fillP = "purple"
                    if(self.board[row][col] == "1"):
                        fillP = "red"
                    elif(self.board[row][col] == "2"):
                        fillP = "blue"
                    elif(self.board[row][col] == "3"):
                        fillP = "green"
                    canvas.create_rectangle(CardBoard.seperationX + \
                                       Card.cardWidth * col - Card.cardWidth // 2,
                                       CardBoard.seperationY + \
                                       Card.cardHeight * row - Card.cardHeight // 2,\
                                       CardBoard.seperationX + \
                                       Card.cardWidth * col + Card.cardWidth // 2,\
                                       CardBoard.seperationY + \
                                       Card.cardHeight * row + Card.cardHeight // 2,\
                                       fill = fillP)

    # Takes a string representation of a temporary piece board and reformats
    # it into a matrix and populates the real piece board 
    def refillPBoard(self, newBoard):
        nB= newBoard[0]
        nB = nB.replace(', ', ',')
        nB = nB.replace('[[', '')
        nB = nB.replace(']]', '')
        nB = nB.replace('[', '')
        nB = nB.replace(']', '')
        nB = nB.replace("'", "")
        nB = nB.split(",")
        counter = 0
        matrixLen = 10
        for row in range(matrixLen):
            for col in range(matrixLen):
                self.board[row][col]= nB[counter]
                counter += 1

# Button Class
class Btn(object):

    # Btn properties 
    def __init__(self, color, message, xPos, yPos, \
                 width = Card.cardWidth * 2, height = Card.cardHeight * 2):
        self.color = color
        self.message = message
        self.width = width
        self.height = height
        self.xPos = xPos
        self.yPos = yPos

    # Draws button 
    def drawBtn(self, canvas):
        canvas.create_rectangle(self.xPos - self.width // 2, \
                                self.yPos - self.height // 2, \
                                self.xPos + self.width // 2, \
                                self.yPos + self.height // 2, \
                                fill = self.color)
        canvas.create_text(self.xPos, self.yPos, text = self.message, \
                           font = "Arial 32 bold", fill = "white")

    # Checks if a button was clicked 
    def buttonClicked(self, xClicked, yClicked):
        leftBound = self.xPos - self.width // 2
        rightBound = self.xPos + self.width // 2
        topBound = self.yPos - self.height // 2
        botBound = self.yPos + self.height // 2
        if(leftBound <= xClicked <= rightBound and \
           topBound <= yClicked <= botBound):
            return True
        return False

# New Card Button (sublass of Button)
class NewCardBtn(Btn):

    # New Card Btn properties 
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.width = Card.cardWidth * 2
        self.height = Card.cardHeight * 2
        # Code structure for images learned from Image module on PIL
        # documentation
        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
        self.imageFile = "playing-card-gifs/x1.gif"
        self.img = Image.open(self.imageFile)
        self.img = self.img.resize((self.width, self.height))
        self.picture = ImageTk.PhotoImage(self.img)

    # When this button is clicked it gives the player a random card from
    # one of the decks
    def buttonAction(self, playerCards, d1, d2):
        tempHand = playerCards.getCards()
        randDeck = random.randint(0, 1)
        if(randDeck == 0):
            card = d1.getRandomCard()
        if(randDeck == 1):
            card = d2.getRandomCard()
        tempHand.append(card)
        return tempHand

    # Overrides Button draw 
    def drawBtn(self, canvas):
        canvas.create_image(self.xPos, self.yPos, image = self.picture)

# Lines of code: 534



        

    
        

    




