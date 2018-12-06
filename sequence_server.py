# Barebones server code acquired from
# https://kdchin.gitbooks.io/sockets-module-manual/
import socket
import threading
from queue import Queue
from sequence import *
import json
import sys
from port_changer import *


HOST = "" # Empty is own computer # put your IP address here if playing on multiple computers

# Reads current port from file
portFile = open("port_number.txt")
lines = portFile.readlines()
initialPort = int(lines[0])
portFile.close()

# Creates new port and populates PORT with value
p = Port(initialPort)
p.getNewPortNum()
p.copyToFile("port_number.txt")
PORT = p.getPortNum() # Change each time you test

# Number of people to connect with server
BACKLOG = 3 

# Creates socket connection to client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

# Takes a string representation of a temporary piece board and reformats
# it into a matrix and populates the real piece board 
def fillPBoard(msg):
    msg = msg.split(" [[")
    matrixMsg = msg[1]      
    matrixMsg = matrixMsg.replace("], [", ", ")
    matrixMsg = matrixMsg.replace("]]", "")
    matrixMsg = matrixMsg.split(", ")
    counter = 0
    matrixLen = 10
    for row in range(matrixLen):
        for col in range(matrixLen):
            if(pBoard.getPlayer(row, col) != '0'):
                if(matrixMsg[counter] == "'0'" or \
                     matrixMsg[counter] == '0'):
                    pBoard.setPlayer(row, col, '0')
                else:
                    pBoard.setPlayer(row, col, pBoard.getPlayer(row, col))
            else:
                if(matrixMsg[counter] == "'1'" or \
                   matrixMsg[counter] == '1'):
                    pBoard.setPlayer(row, col, '1')
                elif(matrixMsg[counter] == "'2'" or \
                     matrixMsg[counter] == '2'):
                    pBoard.setPlayer(row, col, '2')
                elif(matrixMsg[counter] == "'3'" or \
                     matrixMsg[counter] == '3'):
                    pBoard.setPlayer(row, col, '3')
                elif(matrixMsg[counter] == "'0'" or \
                     matrixMsg[counter] == '0'):
                    pBoard.setPlayer(row, col, '0')
            counter += 1

# Gets the nex player
def getNextPlayer(currPlayer):
    if(currPlayer == "1"):
        return "2"
    elif(currPlayer == "2"):
        return "3"
    else:
        return "1"

# Handles client 
def handleClient(client, serverChannel, cID, clientele):
    client.setblocking(1)
    msg = ""
    while True:
        try:
            # Number in recv refers to amount of characters the server
            # accepts from a client message
            msg = client.recv(1024).decode("UTF-8")
            command = msg.split("\n")
            while (len(command) > 1):
                readyMsg = command[0]
                msg = "\n".join(command[1:])
                serverChannel.put(str(cID) + " " + readyMsg)
                command = msg.split("\n")
            tempMsg = command
            tempMsg = command[0].split(" ")
            # If a client won the game it alerts all clients the game
            # is over
            if(tempMsg[0] == "gameOver"):
                msg = "gameOver " + (msg.split(" ")[1]) + "\n"
                for cID in clientele:
                    clientele[cID].send(msg.encode())
            # After a player turn it sends updated board to all clients 
            elif(tempMsg[0] == "playerPlayed"):
                fillPBoard(msg)
                msg = "boardFilled " + str(pBoard) + "\n"
                msg = msg.replace(", ",",")
                for cID in clientele:
                    clientele[cID].send(msg.encode())
            # After a player ends their turn, this finds the next player
            # and updates all the clients of who's turn it is
            elif(tempMsg[0] == "playerEnded"):
                nextPlayer = getNextPlayer(msg.split(" ")[1])
                msg = "nextPlayer " + nextPlayer + "\n"
                for cID in clientele:
                    clientele[cID].send(msg.encode())
            # After a player readies up for the game it let's all clients
            # know so they can identify whether or not to start the game. 
            elif(tempMsg[0] == "playerReady"):
                msg = "playerReady " + msg.split(" ")[1] + "\n"
                for cID in clientele:
                    clientele[cID].send(msg.encode())
        except:
            # we failed
            print("client handle of server failed")
            return

# Server message print out of when it sends a message to the clients
def serverThread(clientele, serverChannel):
    while True:
        msg = serverChannel.get(True, None)
        print("msg recv: ", msg)
        msgList = msg.split(" ")
        senderID = msgList[0]
        instruction = msgList[1]
        details = " ".join(msgList[2:])
        if (details != ""):
            for cID in clientele:
                if cID != senderID:
                    sendMsg = instruction + " " + senderID + " " + \
                              details + "\n"
                    clientele[cID].send(sendMsg.encode())
                    print("> sent to %s:" % cID, sendMsg[:-1])
        print()
        serverChannel.task_done()

# Dictionary of all players
clientele = dict()
# Index for players list
playerNum = 0
# List with players IDs
players = [1, 2, 3]
# Creates server piece board
pBoard = PieceBoard()

# Creates server queue and thread
serverChannel = Queue(100)
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()

# Keeps the connection of the server to client up and running
while True:
    client, address = server.accept()
    # myID is the key to the client in the clientele dictionary
    myID = players[playerNum]
    for cID in clientele:
        print (repr(cID), repr(playerNum))
        clientele[cID].send(("newPlayer %s\n" % myID).encode())
        client.send(("newPlayer %s\n" % cID).encode())
    clientele[myID] = client
    client.send(("myIDis %s \n" % myID).encode())
    print("connection recieved from %s" % myID)
    threading.Thread(target = handleClient, args = 
                        (client, serverChannel, myID, clientele)).start()
    playerNum += 1

# Lines of code: 171
