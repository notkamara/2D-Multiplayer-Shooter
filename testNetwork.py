import network, threading, random
import pygame
from datetime import datetime
width = 800
height = 600

def mainData():
    choice = raw_input("Client(C) or Server(S)?")
    if choice.lower() == "s":
        conn, addr = network.makeServer("192.168.0.3", 1234)
        while True:
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            network.serverSend(str(x) + " " + str(y))
            one = datetime.now()
            data = network.serverReceive(1024)
            two = datetime.now()
            ms = two - one
            ms = ms.seconds * 1000
            print ms
            #data = data.strip(" ")
            #x = data[0]
            #y = data[1]
    else:
        s = network.makeClient("92.239.64.212", 1234)
        while True:
            one = datetime.now()
            data = network.clientReceive(1024)
            two = datetime.now()
            ms = two - one
            ms = ms.seconds * 1000
            #data = data.strip(" ")
            #x = data[0]
            #y = data[1]
            #print str(x) + " " + str(y)
            print ms
            network.clientSend(str(x) + " " + str(y))
            
thread = threading.Thread(target=mainData)
thread.start()
