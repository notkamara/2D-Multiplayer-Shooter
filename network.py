import socket
global s, conn, addr

def makeServer(serverIp, serverPort):
    global s, conn, addr
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((serverIp, 1234))
    s.listen(1)
    conn, addr = s.accept()
    return conn, addr

def makeClient(serverIp, serverPort):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s.connect((serverIp, serverPort))

def serverSend(data):
    conn.send(data)

def serverReceive():
    return conn.recv(1024)

def serverReceive(size):
    return conn.recv(size)

def clientSend(data):
    s.send(data)

def clientReceive():
    return s.recv(1024)

def clientReceive(size):
    return s.recv(size)
