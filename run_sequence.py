
# If txt file with PORT number exists read port number
# generate new PORT number and save into vairiable
# While new port number == old
    # generate new port number until different
#save new port number into file
# Call a subprocess that start server paassing as parameter PORT number
# For 1 to 3
    # call a subprocess that starts a client passing as a parametrt PORT
    # number
##    
##import random
##import subprocess
##import os
## 

##file = open('port_number.txt')
##lines = file.readlines()
##portVal = lines[0]
##file.close()
###print(portVal)
###print(type(portVal))
##
##randPort = random.randint(10000, 99999)
##while(portVal == str(randPort)):
##    randPort = random.randint(10000, 99999)
###print(randPort)
##
##tempFile = open("port_number.txt").read()
##tempFile = tempFile.replace(str(portVal), str(randPort))
##file = open("port_number.txt", 'w')
##file.write(tempFile)
##file.close()
##
##import threading
##import time
##import sequence_server
##import sequence_client
##
##
##sequence_server.main()
##for i in range(3):
##    sequence_client.main()
##print("ended")



##class MyThread(threading.Thread):
##    def run(self):
##        num = self.getName()
##        print(num)
##        if(num == "Thread-1"):
##            import sequence_server.py
##        else:
##            print("running client")
##            import sequence_client.py
##
##for x in range(2):
##    mythread = MyThread(name = x)
##    mythread.start()
##    time.sleep(5)
##
##threads = []
##threads.append(threading.Thread(target = sequence_server.main))
##
##print("Completed joining.")
##
##for x in range(2):
##    threads.append(threading.Thread(target = sequence_client.main))
##
##for t in threads:
##    t.start()
##    time.sleep(5)
##    
    
##import sequence_client.py
##import sequence_client.py
##import sequence_client.py

##
##print("opening")
###pathServer = "sequence_server.py"
##pathServer = "hello_world.py"
##subprocess.Popen(['python', pathServer], stdout=subprocess.PIPE)
##print("after")
#subprocess.Popen([pathServer, str(randPort)])
#os.system("python3 " + pathServer)
#for player in range(3):
#    pathClient = "sequence_client.py"
#    subprocess.Popen(['python', pathClient])
##    
##
##
##
##









    
### # # # # # #



##import random
##class Port():
##
##    def __init__(self, portNum = 10000):
##        self.portNum = portNum
##        self.prevVal = 0
##
##    def getPortNum(self):
##        return self.portNum
##
##    def getNewPortNum(self):
##        self.prevVal = self.portNum
##        randPort = random.randint(10000, 65535)
##        while(self.portNum == randPort):
##            randPort = random.randint(10000, 65535)
##        self.portNum = randPort
##
##    def copyToFile(self, filename):
##        tempFile = open("port_number.txt").read()
##        print("Going to replace "+ str(self.prevVal) + " for " + str(self.portNum))
##        tempFile = tempFile.replace(str(self.prevVal), str(self.portNum))
##        file = open("port_number.txt", 'w')
##        file.write(tempFile)
##        file.close()

    
##    def readPortVal(self):
##        file = open('port_number.txt')
##        lines = file.readlines()
##        self.prevVal = int(lines[0])
##        file.close()
##        #print(portVal)
##        #print(type(portVal))
##
##    def makeNewPortVal():
##        portVal = getPortVal()
##        randPort = random.randint(10000, 99999)
##        while(portVal == str(randPort)):
##            randPort = random.randint(10000, 99999)
##        #print(randPort)
##        file.close()
##
##
##    def replacePortVal():
##        portVal = getPortVal()
##        randPort = makeNewPortVal()
##        tempFile = open("port_number.txt").read()
##        tempFile = tempFile.replace((portVal), (randPort))
##        file = open("port_number.txt", 'w')
##        file.write(tempFile)
##        file.close()

