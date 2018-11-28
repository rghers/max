# Barebone client code acquired from
# https://kdchin.gitbooks.io/sockets-module-manual/

import socket
import threading
from queue import Queue
import json

HOST = "" # put your IP address here if playing on multiple computers
PORT = 10156

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
    print("recieved from server")
    server.setblocking(1)
    msg = ""
    command = ""
    while True:
        msg += server.recv(1024).decode("UTF-8")
        command = msg.split("\n")
        while (len(command) > 1):
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverMsg.put(readyMsg)
            command = msg.split("\n")



from tkinter import *
from sequence import *
import random
####################################
# customize these functions
####################################

# Code acquired from CMU 15-112: Fundamentals of Programming and Computer
# Science Class Notes: Animation Part 2: Time-Based Animations in Tkinter
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

def init(data):
    data.d1 = Deck()
    data.d2 = Deck()
    data.cardBoard = CardBoard()
    data.cardBoard.cardFillBoard()
    data.playerCards = PlayerDeck(data.d1, data.d2)
    data.otherPlayers = dict()
    data.gameOver = False
    data.playedTurn = False
    data.receivedCard = False
    data.pBoard = PieceBoard()
    data.playerID = 0
    data.margin = 200
    data.getCardBtn = NewCardBtn(data.width - 2 * Card.cardWidth, \
                                 data.height // 2 - data.margin // 2)
    data.endTurnBtn = Btn("red", "End Turn", data.width - data.margin, \
                                  data.height - data.margin)
    data.currPlayer = "1"



def mousePressed(event, data):
    msg = ""
    row, col = data.pBoard.convertCoordToPos(event.x, event.y)
    if(data.playerID == data.currPlayer):
        if(data.playerCards.clickedHandCard(event.x, event.y) > 0):
            # get the card
            cardInd = data.playerCards.clickedHandCard(event.x, event.y)
            card = data.playerCards.getCard(cardInd)
            # Find location of card in CardBoard
            positions = data.cardBoard.locateCard(card)
            print(positions)
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
        elif(not data.playedTurn):
            if(data.pBoard.onPieceBoard(row, col) and\
               data.pBoard.isValidPos(row, col) and\
               data.pBoard.isCornerPiece(row, col)):
                data.playedTurn = True
                data.receivedCard = True
                data.pBoard.fillPosInPieceBoard(row, col, \
                                                data.playerID)
                msg = "playerPlayed " + str(data.pBoard)
                print(msg)
            elif(data.pBoard.onPieceBoard(row, col) and\
               data.pBoard.isValidPos(row, col) and\
               (data.playerCards.hasCard(data.cardBoard.getCard(row, col)) or\
                data.playerCards.hasTwoEyedJack())):
                data.playedTurn = True
                data.playerCards.removeCard(data.cardBoard.getCard(row, col), \
                                            "two")
                data.pBoard.fillPosInPieceBoard(row, col, \
                                                data.playerID)
                msg = "playerPlayed " + str(data.pBoard)
                print(msg)
            elif(data.pBoard.onPieceBoard(row, col) and\
                 not data.pBoard.isValidPos(row, col) and\
                 data.playerCards.hasOneEyedJack() and\
                 data.playerID != data.pBoard.getPlayer(row, col)):
                print("entered one eyed jack case")
                data.playedTurn = True
                data.playerCards.removeCard(data.cardBoard.getCard(row, col), \
                                            "one")
                data.pBoard.fillPosInPieceBoard(row, col, "0")
                msg = "playerPlayed " + str(data.pBoard)
                print(msg)
        elif(data.getCardBtn.buttonClicked(event.x, event.y) and \
             not data.receivedCard):
            data.getCardBtn.buttonAction(data.playerCards, data.d1, data.d2)
            data.receivedCard = True
        elif(data.endTurnBtn.buttonClicked(event.x, event.y)):
            data.playedTurn = False
            data.receivedCard = False
            msg = "playerEnded " +  data.playerID 
            print(msg)
        if(msg != ""):
            data.server.send(msg.encode())
    else:
        print("Not your turn")

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
                # I think here i need to get a message from the server
                # saying gameEnded, and rather check after a playerPlayed
                # in mouse clicked if the game is over. If it's over then send
                # a modified message to server so that it can process message
                # and send out to all servers. Then here change gameOver to true
                if(data.pBoard.winningBoard(0, 0)):
                    data.gameOver = True
            elif(command == "boardFilled"):
                # refill players boards
                data.pBoard.refillPBoard(msg[1:])
            elif(command == "nextPlayer"):
                # Transfers move to next player
                data.currPlayer = msg[1]
        except:
            print("failed")
            serverMsg.task_done()

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
        
    
##    class Struct(object): pass
##    data = Struct()
##    data.server = server
##    data.serverMsg = serverMsg
##    data.width = width
##    data.height = height
##    data.timerDelay = 100 # milliseconds
##    # create the root and the canvas
##    root = Tk()
##    # -------- MAKE A SCROLLABLE WINDOW ------------
####    # Define the scroll limits
####    scrollLimitLow=100
####    scrollLimit=300
####    # Define a frame for the root
####    frame=Frame(root,width=scrollLimit,height=scrollLimit)
####    frame.grid(row=0,column=0)
####    # Define scroll region for the Canvas and instantiate in the frame
##    canvas = Canvas(frame, width=data.width, height=data.height, scrollregion=(0,0,data.width+scrollLimitLow,data.height+scrollLimitLow))
####    # Setup properties of scroll bars
####    hbar=Scrollbar(frame,orient=HORIZONTAL)
####    hbar.pack(side=BOTTOM,fill=X)
####    hbar.config(command=canvas.xview)
####    vbar=Scrollbar(frame,orient=VERTICAL)
####    vbar.pack(side=RIGHT,fill=Y)
####    vbar.config(command=canvas.yview)
####    canvas.config(width=data.width-scrollLimit,height=data.height-scrollLimitLow)
####    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
####    canvas.pack(side=LEFT,expand=True,fill=BOTH)
##    # ----------------------------------------------
##    init(data)
##    # set up events
##    root.bind("<Button-1>", lambda event:
##                            mousePressedWrapper(event, canvas, data))
##    root.bind("<Key>", lambda event:
##                            keyPressedWrapper(event, canvas, data))
##    timerFiredWrapper(canvas, data)
##    
##    # and launch the app
##    root.mainloop()  # blocks until window is closed
##    print("bye!")

serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

run(1400, 810, serverMsg, server)
