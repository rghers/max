import random
class Port():

    def __init__(self, portNum = 10000):
        self.portNum = portNum
        self.prevVal = 0

    def getPortNum(self):
        return self.portNum

    def getNewPortNum(self):
        self.prevVal = self.portNum
        randPort = random.randint(10000, 65535)
        while(self.portNum == randPort):
            randPort = random.randint(10000, 65535)
        self.portNum = randPort

    def copyToFile(self, filename):
        tempFile = open("port_number.txt").read()
        print("Going to replace "+ str(self.prevVal) + " for " + str(self.portNum))
        tempFile = tempFile.replace(str(self.prevVal), str(self.portNum))
        file = open("port_number.txt", 'w')
        file.write(tempFile)
        file.close()
