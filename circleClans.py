import pygame, math, network, threading
from pygame.locals import *
global s, decision
def init():
    global s, decision
    decision = raw_input("Would you like to host or connect to a server? H/C:")
    if decision.lower() == "h":
        serverIP = raw_input("Enter the server IP:")
        serverPort = raw_input("Enter the server Port:")  
        conn, addr = network.makeServer(serverIP, serverPort)
        
    elif decision.lower() == "c":
        serverIP = raw_input("Enter the server IP:")
        serverPort = raw_input("Enter the server Port:")  
        s = network.makeClient(serverIP, int(serverPort))
    
    else:
        print "Please pick a valid option."
        init()

init()
pygame.init()

width = 800
height = 600

fps = 30
delta = 1

gameExit = False
bulletInitialised = False
rocketInitialised = False
rocketCounter = 0

ballRadius = 20
ballX = 500
ballY = 300
ballVelocity = 0
ballVX = 0
ballVY = 0

bulletRadius = 10
bulletX = -100
bulletY = -100
bulletVelocity = 15
bulletVX = 0
bulletVY = 0

ball2X = 0
ball2Y = 0
bullet2X = 0
bullet2Y = 0

mouseX = 0
mouseY = 0

sendData = ""
recvData = ""

hitCount = 0

black = (0,0,0)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Circle Clans")
#RECEIVING THREAD-----------------------------------------------------------------
def receiveData():
    while True:
        global s, ball2X, ball2Y, bullet2X, bullet2Y
        if decision.lower() == "h":
            recvData = network.serverReceive(50000)
        else:
            recvData = network.clientReceive(50000)
        recvData = recvData.split(" ")
        ball2X = int(recvData[0])
        ball2Y = int(recvData[1])
        bullet2X = int(recvData[2])
        bullet2Y = int(recvData[3])
thread = threading.Thread(target=receiveData)
thread.start()
#RENDERING------------------------------------------------------------------------
def render():
    global ball2X, ball2Y, bullet2X, bullet2Y
    ballPos = (int(ballX),int(ballY))
    bulletPos = (int(bulletX),int(bulletY))
    ball2Pos = (int(ball2X), int(ball2Y))
    bullet2Pos = (int(bullet2X),int(bullet2Y))
    colour = (255, 0, 0)
    colour2 = (0, 0, 255)
    colour3 = (0,255,0)
    colour4 = (0,255,255)
    
    screen.fill(black)

    pygame.draw.circle(screen, colour4, bullet2Pos, bulletRadius, 0)  
    pygame.draw.circle(screen, colour, bulletPos, bulletRadius, 0)
    pygame.draw.circle(screen, colour2, ballPos, ballRadius, 0)
    pygame.draw.circle(screen, colour3, ball2Pos, ballRadius, 0)
    pygame.display.update()

clock = pygame.time.Clock()

#GAME LOOP STARTS HERE-------------------------------------------------------------
#STARTING THE RECEIVING OF DATA
while not gameExit:
#EVENT HANDLING STARTS HERE--------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == KEYDOWN:
            if event.key == K_UP:
                ballVY = -10
            elif event.key == K_DOWN:
                ballVY = 10
            elif event.key == K_LEFT:
                ballVX = -10
            elif event.key == K_RIGHT:
                ballVX = 10
        if event.type == KEYUP:
            if event.key == K_UP:
                ballVY = 0
            elif event.key == K_DOWN:
                ballVY = 0
            elif event.key == K_LEFT:
                ballVX = 0
            elif event.key == K_RIGHT:
                ballVX = 0
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if bulletInitialised == False and rocketInitialised == False:
                    bulletX = ballX
                    bulletY = ballY
                    bulletVX = ((mouseX - bulletX)/math.sqrt(((mouseX - bulletX)**2)+((mouseY - bulletY)**2)))* bulletVelocity
                    bulletVY = ((mouseY - bulletY)/math.sqrt(((mouseX - bulletX)**2)+((mouseY - bulletY)**2)))* bulletVelocity
                    bulletInitialised = True
            elif event.button == 3:
                if rocketInitialised == False and bulletInitialised == False:
                    rocketCounter = 0
                    bulletX = ballX
                    bulletY = ballY
                    bulletVX = ((mouseX - bulletX)/math.sqrt(((mouseX - bulletX)**2)+((mouseY - bulletY)**2)))* bulletVelocity
                    bulletVY = ((mouseY - bulletY)/math.sqrt(((mouseX - bulletX)**2)+((mouseY - bulletY)**2)))* bulletVelocity
                    rocketInitialised = True
    mouseX, mouseY = pygame.mouse.get_pos()
#END OF EVENT HANDLING-------------------------------------------------------------
#START OF PHYSICS------------------------------------------------------------------
#BULLET VELOCITIES AND LOGIC
    if bulletInitialised == True:
        bulletX += bulletVX
        bulletY += bulletVY
    if rocketInitialised == True:
        bulletX += ((mouseX - bulletX)/math.sqrt(((mouseX - bulletX)**2)+((mouseY - bulletY)**2)))* bulletVelocity
        bulletY += ((mouseY - bulletY)/math.sqrt(((mouseX - bulletX)**2)+((mouseY - bulletY)**2)))* bulletVelocity
        rocketCounter += 1
        if rocketCounter >= 60:
            rocketInitialised = False
            bulletX = -100
            bulletY = -100
    ballX += ballVX
    ballY += ballVY
#COLLISION DETECTION STARTS HERE-----------------------------------------------------
#BULLET COLLISIONS
    if bulletX > width + ballRadius:
        bulletX = -100
        bulletY = -100
        bulletInitialised = False
        rocketInitialised = False
    elif bulletX < 0 - ballRadius:
        bulletX = -100
        bulletY = -100
        bulletInitialised = False
        rocketInitialised = False
    if bulletY > height + ballRadius:
        bulletX = -100
        bulletY = -100
        bulletInitialised = False
        rocketInitialised = False
    elif bulletY < 0 - ballRadius:
        bulletX = -100
        bulletY = -100
        bulletInitialised = False
        rocketInitialised = False
    if math.sqrt(((ball2X - bulletX)**2)+((ball2Y - bulletY)**2))< ballRadius + bulletRadius:
        bulletInitialised = False
        bulletX = -100
        bulletY = -100
    if rocketInitialised == True:
        if math.sqrt(((mouseX - bulletX)**2)+((mouseY - bulletY)**2))< bulletRadius:
                bulletInitialised = False
                bulletX = -100
                bulletY = -100
#BALL COLLISIONS
    if ballX > width - ballRadius:
        ballX = width - ballRadius
        ballVX = 0
    elif ballX < 0 + ballRadius:
        ballX = 0 + ballRadius
        ballVX = 0
    if ballY > height - ballRadius:
        ballY = height - ballRadius
        ballVY = 0
    elif ballY < 0 + ballRadius:
        ballY = 0 + ballRadius
        ballVY = 0
    if math.sqrt(((ballX - bullet2X)**2)+((ballY - bullet2Y)**2))< ballRadius + bulletRadius:
        hitCount += 1
        print("You got hit b0ss " + str(hitCount))
#END OF COLLISION DETECTION------------------------------------------------------------
#END OF PHYSICS------------------------------------------------------------------------
#NETWORKING
    global decision
    sendData = str(ballX)+" "+str(ballY)+" "+str(bulletX)+" "+str(bulletY)
    if decision.lower() == "h":
        network.serverSend(sendData)
    else:
        network.clientSend(sendData)
    render()
    clock.tick(fps)
    print(clock.get_fps())
#GAME LOOP ENDS HERE-------------------------------------------------------------------
pygame.quit()
global s, conn
if decision.lower() == "h":
    conn.close()
else:
    s.close()
quit()
