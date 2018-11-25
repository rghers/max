import socket
import threading
from queue import Queue
import json

HOST = "" # put your IP address here if playing on multiple computers
PORT = 10008

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

# events-example0.py from 15-112 website
# Barebones timer, mouse, and keyboard events

from tkinter import *
from sequence import *
import random
####################################
# customize these functions
####################################

def init(data):
    data.d1 = Deck()
    data.d2 = Deck()
##    data.d1.cardFillDeck()
##    data.d2.cardFillDeck()
    data.cardBoard = CardBoard()
    data.cardBoard.cardFillBoard()
    data.playerCards = PlayerDeck(data.d1, data.d2)
    data.otherPlayers = dict()
    data.gameOver = False
    data.playedTurn = False
    data.pBoard = PieceBoard()
    data.playerID = 0

def endTurnClicked(data, x, y):
    return (data.width - 50 <= x <= data.width and\
            data.height - 50 <= y <= data.height)

def mousePressed(event, data):
    msg = ""
    row,col = data.pBoard.convertCoordToPos(event.x, event.y)
    if(not data.playedTurn):
        if(data.pBoard.onPieceBoard(row, col) and\
           data.pBoard.isValidPos(row, col) and\
           (data.playerCards.hasCard(data.cardBoard.getCard(row, col)) or\
            data.playerCards.hasTwoEyedJack())):
            data.playedTurn = True
            data.playerCards.removeCard(data.cardBoard.getCard(row, col))
            data.pBoard.fillPosInPieceBoard(row, col, \
                                            data.playerID)
            
            #data.cardBoard.getCard(row,col).convertColor()
            #data.cardBoard.modifyCardColor(row, col, \
                                           #data.players[data.playerInd])
##            data.cardBoard.getCard(row, col).convertColor(\
##                data.players[data.playerInd])
            data.pBoard.printBoard()
            print()
            #msg = "playerPlayed "+json.dumps(data.pBoard)
            msg = "playerPlayed " + str(data.pBoard)
            print(msg)
        elif(data.pBoard.onPieceBoard(row, col) and\
             not data.pBoard.isValidPos(row, col) and\
             data.playerCards.hasOneEyedJack() and\
             data.playerID != data.pBoard.getPlayer(row, col)):
            data.playedTurn = True
            data.playerCards.removeCard(data.cardBoard.getCard(row, col))
            data.pBoard.fillPosInPieceBoard(row, col, 0)
            #msg = "playerPlayed "+json.dumps(data.pBoard)
            msg = "playerPlayed " + str(data.pBoard)
            print(msg)
        elif(endTurnClicked(data, event.x, event.y)):
            data.playedTurn = False
            msg = "playerEnded"
            print(msg)
        if(msg != ""):
            data.server.send(msg.encode())

def keyPressed(event, data):
    pass

def timerFired(data):
    while (serverMsg.qsize() > 0):
        msg = serverMsg.get(False)
        try:
            print("received: ", msg, "\n")
            msg = msg.split()
            command = msg[0]
            if(command == "myIDis"):
                data.playerID = msg[1]
            elif(command == "newPlayer"):
                newPID = msg[1]
                data.otherPlayers[newPID] = PlayerDeck(data.d1, data.d2)
            elif(command == "playerPlayed"):
                jsonValue = msg[1]
                if(data.pBoard.winningBoard(0, 0)):
                    data.gameOver = True
            elif(command == "playerEnded"):
                # Transfers move to next player
                print("Player ended turn")
        except:
            print("failed")
            serverMsg.task_done()

def redrawAll(canvas, data):
    if(data.gameOver):
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "red")
    else:
        #canvas.create_image(0, 0, anchor = NW, \
        #                    image = data.pokerTableImg)
        data.cardBoard.drawBoard(canvas)
        ## Temp State ##
        data.pBoard.drawPieces(canvas)
        ## END ## 
        data.playerCards.drawDeck(canvas)
        canvas.create_rectangle(data.width - 50, data.height - 50, \
                                data.width, data.height)

####################################
# use the run function as-is
####################################

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
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
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

serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

run(1400, 810, serverMsg, server)
