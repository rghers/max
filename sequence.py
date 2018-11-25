# oopy-playing-cards-demo.py
# Demos class attributes, static methods, repr, eq, hash
from tkinter import *
from PIL import Image, ImageTk, ImageOps
import random

# Adapted from course notes of OOPy 
class Card(object):
    numberNames = [None, "Ace", "2", "3", "4", "5", "6", "7",
                   "8", "9", "10", "Jack", "Queen", "King"]
    suitNames = ["Clubs", "Diamonds", "Hearts", "Spades"]
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3
    cardHeight = 71
    cardWidth = 96
    
    def __init__(self, number, suit):
        # number is 1 for Ace, 2...10,
        #           11 for Jack, 12 for Queen, 13 for King
        # suit is 0 for Clubs, 1 for Diamonds,
        #         2 for Hearts, 3 for Spades
        self.number = number
        self.suit = suit
        # http://zetcode.com/gui/tkinter/drawing/
        self.filename = "playing-card-gifs/%s%d.gif" % \
                        (Card.suitNames[self.suit][0].lower(),\
                         self.number)
        
        self.img = Image.open(self.filename)
        self.img = self.img.resize((Card.cardWidth, Card.cardHeight))
        self.picture = ImageTk.PhotoImage(self.img)
        

    def __repr__(self):
        return ("<%s of %s>" %
                (Card.numberNames[self.number],
                 Card.suitNames[self.suit]))

    def getHashables(self):
        return (self.number, self.suit) # return a tuple of hashables

    def __hash__(self):
        return hash(self.getHashables())

    def __eq__(self, other):
        return (isinstance(other, Card) and
                (self.number == other.number) and
                (self.suit == other.suit))

    # Retrieved from images demo in Animation Demos course notes

    def getSpecialPlayingCardImage(self, name):
        specialNames = ["back", "joker1", "joker2"]
        return getPlayingCardImage(data, specialNames.index(name)+1, "x")

    def drawPlayingCard(self, canvas, xPos, yPos):
        canvas.create_image(xPos, yPos, image = self.picture)

##    def givePiece(self, player):
##        currentImage = self.img
##        newImage = self.convertColor(player)
##        self.picture = ImageTk.PhotoImage(newImage)

    def convertColor(self, player):
        if(player == 0):
            return self.img
        tempImage = self.img
        for i in range(self.cardWidth):
            for j in range(self.cardHeight):
                pixel = tempImage.getpixel((i, j))
                if(i == 0 and j == 0):
                    print(pixel)
               # if(pixel == (256, 256, 256)):
                    #print("found white pixel")
                if(player == 1):
                    tempImage.putpixel((i, j), (125, 0, 0))
                elif(player == 2):
                    tempImage.putpixel((i, j), (0, 125, 0))
                elif(player == 3):
                    tempImage.putpixel((i, j), (0, 0, 125))
        return tempImage

    #def convertColor(self, player, white = "#000099", black = "#99CCFF"):
        #temp = self.img
        #tempImage = ImageOps.colorize(ImageOps.grayscale(self.img), black, white)
        #newImage = tempImage.convert('P', palette=Image.ADAPTIVE, colors=256)
        #return newImage
                

##    def manipulatePixels(self, rgbTup):
##        pixels = self.load()
##        for i in range(self.size[0]):
##            for j in range(self.size[1]):
##                rPixel, bPixel, gPixel = pixels[i, j]
##                newRGB = (rPixel + rgbTup[0], bPixel + rgbTup[1], \
##                          gPixel + rgbTup[2])
##                pixels[i, j] = newRGB
##        

    #def cardClickedAction

##    def getValue(self):
##        return self.number
##
##    def getSuit(self):
##        return self.suit
##        
        
class Deck(object):

    def __init__(self):
        self.deck = self.createDeck()
        self.usedCards = set()

    def createDeck(self):
        cards = []
        for rank in range(len(Card.numberNames)):
            for suit in range(len(Card.suitNames)):
                if(rank != 0):
                    card = Card(rank, suit)
                    cards.append(card)
        return cards
    
    def getRandomCard(self):
        randCardIndex = random.randint(0, 51)
        while(self.deck[randCardIndex] in self.usedCards):
            randCardIndex = random.randint(0, 51)
        self.usedCards.add(self.deck[randCardIndex])
        return self.deck[randCardIndex]

    def shuffleDeck(self):
        random.shuffle(self.deck)

    def __repr__(self):
        return "Deck is: \n" + str(self.deck)

    


class CardBoard(object):
    amtRows = 10
    amtCols = 10
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

    def __init__(self):
        self.board = CardBoard.board
        

    def cardFillBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if(self.board[row][col] == (-1, -1)):
                    self.board[row][col] = Card(1, 3)
                else:
                    self.board[row][col] = Card(self.board[row][col][0],\
                                            self.board[row][col][1])

    ## IDEA FOR CHANGING CARDS COLOR OPACITY AFTER A VALID CLICK THEN REDRAWING
    ## IN REDRAWALL AND KEEPING DRAWBOARD SAME. 
    def modifyCardColor(self, row, col, player):
        card = self.board[row][col]
        ## Card Convertion Section ## 
        newCard = card.convertColor(player)
        self.board[row][col] = newCard

    def drawBoard(self, canvas, pieceBoard):
        for row in range(CardBoard.amtRows):
            for col in range(CardBoard.amtCols):
                card = self.board[row][col]
                #card.img = card.convertColor(pieceBoard.getPlayer(row, col))
                #card.givePiece(pieceBoard.getPlayer(row, col))
                card.drawPlayingCard(canvas, CardBoard.seperationX + \
                                     Card.cardWidth * col, \
                                     CardBoard.seperationY + \
                                     Card.cardHeight * row)
                

##    @staticmethod
##    def getBoardDimensions(self):
##        return(CardBoard.amtRows*Card.cardHeight, \
##               CardBoard.amtCols*Card.cardWidth)



        
            

    def getCard(self, row, col):
        return self.board[row][col]

class PlayerDeck(object):

    def __init__(self, cardDeck1, cardDeck2):
        self.cardDeck1 = cardDeck1
        self.cardDeck2 = cardDeck2
        self.amtCards = 6
        self.playerCards = self.giveStaringCards(self.cardDeck1, \
                                                 self.cardDeck2)
        

    def giveStaringCards(self, cardDeck1, cardDeck2):
        tempHand = []
        for i in range(self.amtCards):
            if(i % 2 == 0):
                card = self.cardDeck1.getRandomCard()
            else:
                card = self.cardDeck2.getRandomCard()
            tempHand.append(card)
        return tempHand
    
    def getCards(self):
        return self.playerCards

    def drawDeck(self, canvas):
        x = 125
        y = 775
        for card in self.playerCards:
            card.drawPlayingCard(canvas, x, y)
            x += 150
    
    def hasCard(self, selectedCard):
        for card in self.playerCards:
            if(card == selectedCard):
                return True
        return False

    def hasTwoEyedJack(self):
        s = {Card(11, 0), Card(11, 1)}
        for card in self.playerCards:
            if(card in s):
                return True
        return False

    def hasOneEyedJack(self):
        s = {Card(11, 2), Card(11, 3)}
        for card in self.playerCards:
            if(card in s):
                return True
        return False
            
    def removeCard(self, selectedCard):
        for cardInd in range(len(self.playerCards)):
            if(self.playerCards[cardInd] == selectedCard):
                self.playerCards.pop(cardInd)
                return
        for cardInd in range(len(self.playerCards)):
            s = {Card(11, 0), Card(11, 1), Card(11, 2), Card(11, 3)}
            if(self.playerCards[cardInd] in s):
                self.playerCards.pop(cardInd)
                return
        
        
class PieceBoard(object):
    amtRows = 10
    amtCols = 10
    board = [[0] * CardBoard.amtCols for row in range(CardBoard.amtRows)]

    def __init__(self):
        self.board = PieceBoard.board

    def convertCoordToPos(self, xCoord, yCoord):
        topLeftX = CardBoard.seperationX - Card.cardWidth // 2
        topLeftY = CardBoard.seperationY - Card.cardHeight // 2
        x = xCoord - topLeftX
        y = yCoord - topLeftY
        return (y // Card.cardHeight, x // Card.cardWidth)

    def onPieceBoard(self, row, col):
        return (0 <= row < PieceBoard.amtRows and \
                0 <= col < PieceBoard.amtCols)
    
    def fillPosInPieceBoard(self, row, col, playerNum):
        self.board[row][col] = playerNum

    def isValidPos(self, row, col):
        return self.board[row][col] == 0

    def printBoard(self):
        print(self.board)

    def winningBoard(self, row, col):
        if(row >= len(self.board)):
            return False
        elif(self.board[row][col] == 0):
            newRow, newCol = self.findNextRC(row, col)
            return self.winningBoard(newRow, newCol)
        elif(self.diagConsecutive(row, col) or\
           self.horizConsecutive(row, col) or\
           self.vertConsecutive(row, col)):
            return True
        else:
            newRow, newCol = self.findNextRC(row, col)
            return self.winningBoard(newRow, newCol)

    def findNextRC(self, row, col):
        if(col + 1 == len(self.board[0])):
            return (row+1, 0)
        return (row, col+1)

    def inBounds(self, row, col):
        return (0 <= row < len(self.board) and \
                0 <= col < len(self.board[0]))
        
    def diagConsecutive(self, row, col):
        totalCons = 4
        for i in range(totalCons):
            if(not self.inBounds(row + i + 1, col + i + 1)):
                return False
            elif(not self.board[row + i][col + i] == \
               self.board[row + i + 1][col + i + 1]):
                return False
        return True

    def horizConsecutive(self, row, col):
        totalCons = 4
        for i in range(totalCons):
            if(not self.inBounds(row, col + i + 1)):
                return False
            elif(not self.board[row][col + i] == \
               self.board[row][col + i + 1]):
                return False
        return True

    def vertConsecutive(self, row, col):
        totalCons = 4
        for i in range(totalCons):
            if(not self.inBounds(row + i + 1, col)):
                return False
            elif(not self.board[row + i][col] == \
               self.board[row + i + 1][col]):
                return False
        return True

    def getPlayer(self, row, col):
        return self.board[row][col]


    ## TEMP STATE ##
    def drawPiece(self, canvas):
        for row in range(PieceBoard.amtRows):
            for col in range(PieceBoard.amtCols):
                if(self.board[row][col] != 0):
                    if(self.board[row][col] == 1):
                        fillP = "red"
                    elif(self.board[row][col] == 2):
                        fillP = "blue"
                    elif(self.board[row][col] == 3):
                        fillP = "green"
                    canvas.create_oval(CardBoard.seperationX + Card.cardWidth * col - 10,\
                                       CardBoard.seperationY + Card.cardHeight * row - 10,\
                                       CardBoard.seperationX + Card.cardWidth * col + 10,\
                                       CardBoard.seperationY + Card.cardHeight * row + 10,\
                                       fill = fillP)
    ## END ## 


        

    
