from tkinter import *
from sequence import *
import random

####################################
# customize these functions
####################################


def init(data):
    data.d1 = Deck()
    data.d2 = Deck()
    data.pBoard = PieceBoard()
    data.playerCards = PlayerDeck(data.d1, data.d2)
    data.cardBoard = CardBoard()
    data.cardBoard.cardFillBoard()
    data.players = [1, 2, 3]
    data.playerInd = random.randint(0, len(data.players) - 1)
    data.gameOver = False
    data.playedTurn = False
##    data.pokerTable = Image.open("poker_table.jpeg")
##    data.pokerTable = data.pokerTable.resize((data.width, data.height))
##    data.pokerTableImg = ImageTk.PhotoImage(data.pokerTable)
    

def endTurnClicked(data, x, y):
    return (data.width - 50 <= x <= data.width and\
            data.height - 50 <= y <= data.height)

def mousePressed(event, data):
    row,col = data.pBoard.convertCoordToPos(event.x, event.y)
    if(not data.playedTurn):
        if(data.pBoard.onPieceBoard(row, col) and\
           data.pBoard.isValidPos(row, col) and\
           (data.playerCards.hasCard(data.cardBoard.getCard(row, col)) or\
            data.playerCards.hasTwoEyedJack())):
            data.playedTurn = True
            data.playerCards.removeCard(data.cardBoard.getCard(row, col))
            data.pBoard.fillPosInPieceBoard(row, col, \
                                            data.players[data.playerInd])
            #data.cardBoard.getCard(row,col).convertColor()
            #data.cardBoard.modifyCardColor(row, col, \
                                           #data.players[data.playerInd])
##            data.cardBoard.getCard(row, col).convertColor(\
##                data.players[data.playerInd])
            data.pBoard.printBoard()
            print()
            
        elif(data.pBoard.onPieceBoard(row, col) and\
             not data.pBoard.isValidPos(row, col) and\
             data.playerCards.hasOneEyedJack() and\
             data.players[data.playerInd] != data.pBoard.getPlayer(row, col)):
            data.playedTurn = True
            data.playerCards.removeCard(data.cardBoard.getCard(row, col))
            data.pBoard.fillPosInPieceBoard(row, col, 0)
    
    elif(endTurnClicked(data, event.x, event.y)):
        data.playerInd = (data.playerInd + 1) % len(data.players)
        data.playedTurn = False
    

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    if(data.pBoard.winningBoard(0, 0)):
        data.gameOver = True

def redrawAll(canvas, data):
    if(data.gameOver):
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "red")
    else:
        #canvas.create_image(0, 0, anchor = NW, \
        #                    image = data.pokerTableImg)
        data.cardBoard.drawBoard(canvas, data.pBoard)
        ## Temp State ##
        data.pBoard.drawPieces(canvas)
        ## END ## 
        data.playerCards.drawDeck(canvas)
        canvas.create_rectangle(data.width - 50, data.height - 50, \
                                data.width, data.height)
        

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
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
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
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

run(1400, 810)

