
# ADD REPLAYABILITY
# ADD SOUNDS MAYBE
# ADD RULES PAGE
# ADD AI





# Barebone client code acquired from
# https://kdchin.gitbooks.io/sockets-module-manual/

import socket
import threading
from queue import Queue
import json
from tkinter import *
from sequence import *
import random
#from sequence_AI import * 

HOST = "" # put your IP address here if playing on multiple computers

# Reads port number from a file and populates PORT
portFile = open("port_number.txt")
lines = portFile.readlines()
PORT = int(lines[0])
portFile.close()

# Creates server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connects client to server
server.connect((HOST,PORT))
print("connected to server")

# Receives server message
def handleServerMsg(server, serverMsg):
    print("recieved from server")
    server.setblocking(1)
    msg = ""
    command = ""
    while True:
        # Number in recv refers to amount of characters the client accepts from
        # a server message
        msg += server.recv(1024).decode("UTF-8")
        command = msg.split("\n")
        while (len(command) > 1):
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverMsg.put(readyMsg)
            command = msg.split("\n")

# Code acquired from CMU 15-112: Fundamentals of Programming and Computer
# Science Class Notes: Animation Part 2: Time-Based Animations in Tkinter
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# Sets up the data for the client 
def init(data):
    # Data for 2 decks
    data.d1 = Deck()
    data.d2 = Deck()
    # Data for populated board of all the cards
    data.cardBoard = CardBoard()
    data.cardBoard.cardFillBoard()
    # Data for players hand
    data.playerCards = PlayerDeck(data.d1, data.d2)
    data.otherPlayers = dict()
    # Data for boolean statements 
    data.gameOver = False
    data.playedTurn = False
    data.receivedCard = False
    data.startGameScreen = True
    # Data for creation of piece board
    data.pBoard = PieceBoard()
    # Data for holding client player numbers
    data.playerID = 0
    data.currPlayer = "1"
    data.winner = "0"
    # Data for drawing purposes
    data.margin = 200
    # Data for all buttons created
    data.getCardBtn = NewCardBtn(data.width - 2 * Card.cardWidth, \
                                 data.height // 2 - data.margin // 2)
    data.endTurnBtn = Btn("red", "End Turn", data.width - data.margin, \
                                  data.height - data.margin)
    data.singlePlayerBtn = Btn("blue", "Single Player", data.margin * 2, \
                            data.margin * 2)
    data.multiPlayerBtn = Btn("blue", "MultiPlayer", data.width - \
                              data.margin * 2, data.margin * 2)
    data.rulesBtn = Btn("blue", "Rules", data.width // 2, \
                            data.margin * 3)
    # Data for connectivity of players to the server
    data.readyPlayers = [False, False, False]

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
    msg = ""
    # Splash screen boolean statement for home screen
    if(data.startGameScreen):
        # If client clicks single player we call the sequence_AI file
        if(data.singlePlayerBtn.buttonClicked(event.x, event.y)):
            import sequence_AI
        # If player clicks mulitplayer we connect them to the server
        elif(data.multiPlayerBtn.buttonClicked(event.x, event.y)):
            msg = "playerReady " + data.playerID
            print(data.playerID + "clicked start game")
    else:
        # Checks if it's this players turn
        if(data.playerID != '0' and\
             data.playerID == data.currPlayer):
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
                    msg = "playerPlayed " + str(data.pBoard)
                    if(data.pBoard.winningBoard(0, 0)):
                        msg = "gameOver " + data.playerID
                    print(msg)
                # Checks if a player played a piece in a non-corner position
                elif(data.pBoard.onPieceBoard(row, col) and\
                   data.pBoard.isValidPos(row, col) and\
                   (data.playerCards.hasCard(data.cardBoard.getCard(row, col)) or\
                    data.playerCards.hasTwoEyedJack())):
                    playerPlayedPiece(data, row, col)
                    msg = "playerPlayed " + str(data.pBoard)
                    if(data.pBoard.winningBoard(0, 0)):
                        msg = "gameOver " + data.playerID
                    print(msg)
                # Checks if a player tried to remove someone else's piece
                elif(data.pBoard.onPieceBoard(row, col) and\
                     not data.pBoard.isValidPos(row, col) and\
                     data.playerCards.hasOneEyedJack() and\
                     data.playerID != data.pBoard.getPlayer(row, col)):
                    playerRemovedPiece(data, row, col)
                    msg = "playerPlayed " + str(data.pBoard)
                    print(msg)
            # Checks if a player wants to get a new card after playing a turn
            elif(data.getCardBtn.buttonClicked(event.x, event.y) and \
                 not data.receivedCard):
                data.getCardBtn.buttonAction(data.playerCards, data.d1, data.d2)
                data.receivedCard = True
            # Checks if a player wants to end their turn
            elif(data.endTurnBtn.buttonClicked(event.x, event.y)):
                data.playedTurn = False
                data.receivedCard = False
                msg = "playerEnded " +  data.playerID 
                print(msg)
    # Sends message to server
    if(msg != ""):
        data.server.send(msg.encode())

# Key pressed event
def keyPressed(event, data):
    pass

# Timer fired event
def timerFired(data):
    while (serverMsg.qsize() > 0):
        # Gets server message
        msg = serverMsg.get(False)
        try:
            print("received: ", msg, "\n")
            msg = msg.split()
            command = msg[0] 
            if(command == "myIDis"):
                data.playerID = msg[1]
            # Checks if connecting new player 
            elif(command == "newPlayer"):
                newPID = msg[1]
                data.otherPlayers[newPID] = PlayerDeck(data.d1, data.d2)
            # Checks if game is over
            elif(command == "gameOver"):
                data.gameOver = True
                data.winner = msg[1]
            # Refill players boards
            elif(command == "boardFilled"):
                data.pBoard.refillPBoard(msg[1:])
            # Transfers move to next player
            elif(command == "nextPlayer"):
                data.currPlayer = msg[1]
            # Waits for all players to connect
            elif(command == "playerReady"):
                data.readyPlayers[int(msg[1]) - 1] = True
                if(False not in data.readyPlayers):
                    data.startGameScreen = False
        except:
            print("failed")
            serverMsg.task_done()

# Displays whose player turn it is
def displayPlayerTurn(canvas, data):
    textX = data.width - data.margin
    textY = data.margin // 2
    if(data.currPlayer == "1" and data.playerID == "1"):
        canvas.create_text(textX, textY, text = "Your Turn", \
                           font = "Arial 32 bold", fill = "red")
    elif(data.currPlayer == "2" and data.playerID == "2"):
        canvas.create_text(textX, textY, text = "Your Turn", \
                           font = "Arial 32 bold", fill = "blue")
    elif(data.currPlayer == "3" and data.playerID == "3"):
        canvas.create_text(textX, textY, text = "Your Turn", \
                           font = "Arial 32 bold", fill = "green")
    elif(data.currPlayer == "1"):
        canvas.create_text(textX, textY, text = "Player 1's Turn", \
                           font = "Arial 32 bold", fill = "red")
    elif(data.currPlayer == "2"):
        canvas.create_text(textX, textY, text = "Player 2's Turn", \
                           font = "Arial 32 bold", fill = "blue")
    else:
        canvas.create_text(textX, textY, text = "Player 3's Turn", \
                           font = "Arial 32 bold", fill = "green")

# Draws the winner screen
def drawWinnerScreen(canvas, data):
    if(data.winner == "1"):
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "red")
    elif(data.winner == "2"):
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "blue")
    else:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "green")
    if(data.winner == data.playerID):
        canvas.create_text(data.width // 2, data.height // 2, \
                           text = "You Won!", font = "Arial 32 bold", \
                           fill = "white")
    else:
        canvas.create_text(data.width // 2, data.height // 2, \
                           text = "You Lost. Player " + data.winner + " won", \
                           font = "Arial 32 bold", fill = "white")

# Draws the start screen
def drawStartScreen(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, outline = "blue", \
                           width = 20)
    canvas.create_text(data.width // 2, data.margin, text = "Sequence", \
                       font = "Times 128", fill = "blue")
    data.singlePlayerBtn.drawBtn(canvas)
    data.multiPlayerBtn.drawBtn(canvas)
    data.rulesBtn.drawBtn(canvas)

# Redraw all event
def redrawAll(canvas, data):
    # Draws start game splash screen
    if(data.startGameScreen):
        drawStartScreen(canvas, data)
        if(data.readyPlayers[int(data.playerID) - 1]):
            canvas.create_text(data.width - data.margin * 1.5, \
                               data.height - 50,\
                               text = "Waiting for players...", \
                               font = "Times 64")
    # Draws game over splash screen
    elif(data.gameOver):
        drawWinnerScreen(canvas, data)
    # Draws game state splash screen
    else:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "#1c263d")
        data.cardBoard.drawBoard(canvas)
        data.pBoard.drawPieces(canvas)
        data.playerCards.drawDeck(canvas)
        data.getCardBtn.drawBtn(canvas)
        displayPlayerTurn(canvas, data)
        data.endTurnBtn.drawBtn(canvas)
        

####################################
# use the run function as-is
####################################

# Run function acquired from CMU 15-112: Fundamentals of Programming and
# Computer Science Class Notes: Animation Part 2: Time-Based Animations in
# Tkinter
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

def run(width, height, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
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
        # add title to board
        root.title("Player: "+str(data.playerID))
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data 
    class Struct(object): pass
    data = Struct()
    data.server = server
    data.serverMsg = serverMsg
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # call init after if not imaging error will occur
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
        
# Creates queue and thread    
serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

# Runs client 
run(1400, 810, serverMsg, server)

# Lines of code: 377
