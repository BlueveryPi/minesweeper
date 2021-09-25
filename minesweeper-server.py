#!/usr/bin/env python3

from socket import *
import threading
import platform

connections=[]
players=[]
spectators=[]
def acceptall():
    while True:
        connectionSocket, addr = serverSocket.accept()
        if len(players)<3:
            players.append(connectionSocket)
        else:
            spectators.append(connectionSocket)
        thisguysnick=connectionSocket.recv(1024)
        print(thisguysnick.decode('utf-8'))
        for sock in connections:
            if sock != connectionSocket:
                sock.send(thisguysnick)
        connections.append(connectionSocket)
        sender = threading.Thread(target=send)
        receiver = threading.Thread(target=recv, args=(connectionSocket, ))
        sender.start()
        receiver.start()

def send():
    while True:
        sendData = input("")
        if sendData != "serveroff":
            for sock in players:
                sock.send()
        else:
            serverSocket.close() 

def recv(sock):
    while True:
        data=sock.recv(1024)
        for sock1 in connections:
            if sock1 != sock:
                sock1.send(data)


host = "127.0.0.1"#platform.uname()[1]
port = 65432

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind( (host, port))
serverSocket.listen(1)
print("=== 대기중입니다.")

acceptall()

'''
한 개의 접속만 유지하는 채팅 서버 프로그램
    - 간단, 
'''