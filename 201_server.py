#!/usr/bin/env python3

from socket import *
import threading
import time

connections=[]
def acceptall():
    while True:
        connectionSocket, addr = serverSocket.accept()
        thisguysnick=connectionSocket.recv(1024)
        print(f"{thisguysnick.decode('utf-8')}님이 접속했습니다.")
        for sock in connections:
            if sock != connectionSocket:
                sock.send((f"{thisguysnick.decode('utf-8')}님이 접속했습니다.").encode('utf-8'))
        connections.append(connectionSocket)
        sender = threading.Thread(target=send, args=(connections, ))
        receiver = threading.Thread(target=recv, args=(connectionSocket, connections, ))
        sender.start()
        receiver.start()

def send(socks):
    while True:
        sendData = input("")
        if sendData != "serveroff":
            for sock in socks:
                sock.send(("<System>: "+sendData).encode('utf-8'))
        else:
            serverSocket.close() 

def recv(sock, socks):
    while True:
        data=sock.recv(1024)
        print(data.decode('utf-8'))
        for sock1 in socks:
            if sock1 != sock:
                sock1.send(data)

host = '127.0.0.1'
port = 65432

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind( (host, port))
serverSocket.listen(1)
print("=== 대기중입니다.")

acceptall()
