
# If txt file with PORT number exists read port number
# generate new PORT number and save into vairiable
# While new port number == old
    # generate new port number until different
#save new port number into file
# Call a subprocess that start server paassing as parameter PORT number
# For 1 to 3
    # call a subprocess that starts a client passing as a parametrt PORT
    # number
    
import random
import subprocess

file = open('port_number.txt')
lines = file.readlines()
portVal = lines[0]
file.close()
#print(portVal)
#print(type(portVal))

randPort = random.randint(10000, 99999)
while(portVal == str(randPort)):
    randPort = random.randint(10000, 99999)
#print(randPort)

tempFile = open("port_number.txt").read()
tempFile = tempFile.replace(str(portVal), str(randPort))
file = open("port_number.txt", 'w')
file.write(tempFile)
file.close()

pathServer = "/Users/MaxDunaevschi/Desktop/CMU - First year/CS/Term Project/TP3/sequence_server.py"
subprocess.Popen([pathServer, str(randPort)])
#for player in range(3):
    
    






