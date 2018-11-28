# Barebones server code acquired from
# https://kdchin.gitbooks.io/sockets-module-manual/

import socket
import threading
from queue import Queue
from sequence import *
import json

HOST = "" # Empty is own computer # put your IP address here if playing on multiple computers
PORT = 10156 # Change each time you test
BACKLOG = 3 # number of people

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

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

def getNextPlayer(currPlayer):
    if(currPlayer == "1"):
        return "2"
    elif(currPlayer == "2"):
        return "3"
    else:
        return "1"

def handleClient(client, serverChannel, cID, clientele):
    client.setblocking(1)
    msg = ""
    while True:
        try:
            msg = client.recv(1024).decode("UTF-8")
            command = msg.split("\n")
            while (len(command) > 1):
                readyMsg = command[0]
                msg = "\n".join(command[1:])
                serverChannel.put(str(cID) + " " + readyMsg)
                command = msg.split("\n")
            tempMsg = command
            tempMsg = command[0].split(" ")
            if(tempMsg[0] == "playerPlayed"):
                fillPBoard(msg)
                msg = "boardFilled " + str(pBoard) + "\n"
                msg = msg.replace(", ",",")
                for cID in clientele:
                    clientele[cID].send(msg.encode())
            elif(tempMsg[0] == "playerEnded"):
                nextPlayer = getNextPlayer(msg.split(" ")[1])
                msg = "nextPlayer " + nextPlayer + "\n"
                for cID in clientele:
                    clientele[cID].send(msg.encode())
        except:
            # we failed
            print("client handle of server failed")
            return

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

clientele = dict()
playerNum = 0

pBoard = PieceBoard()
gameOver = False

serverChannel = Queue(100)
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()

players = [1, 2, 3]

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
                        (client ,serverChannel, myID, clientele)).start()
    playerNum += 1
