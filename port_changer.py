import random

# Port class 
class Port():

    # Port properties
    def __init__(self, portNum = 10000):
        self.portNum = portNum
        self.prevVal = 0

    # Getter for port number
    def getPortNum(self):
        return self.portNum

    # Saves old port number and calculates a new number while also ensuring
    # it is different from original value
    def getNewPortNum(self):
        self.prevVal = self.portNum
        randPort = random.randint(10000, 65535)
        while(self.portNum == randPort):
            randPort = random.randint(10000, 65535)
        self.portNum = randPort
        
    # Stores new port number in file
    def copyToFile(self, filename):
        tempFile = open("port_number.txt").read()
        tempFile = tempFile.replace(str(self.prevVal), str(self.portNum))
        file = open("port_number.txt", 'w')
        file.write(tempFile)
        file.close()

# Lines of code: 30
