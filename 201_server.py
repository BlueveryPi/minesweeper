#!/usr/bin/env python3

from socket import *
import threading
import time 

def send(sock):
    while True:
        sendData = input(">>> ")
        if sendData != "close":
            sock.send(sendData.encode("utf-8"))
        else:
            serverSocket.close() 

def recv(sock):
    while True:
        data = sock.recv(1024)
        print("\n상대방1:", data.decode("utf-8"))
        print(">>> ")

host = '127.0.0.1'
port = 65432

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind( (host, port))
serverSocket.listen(1)
print("=== 대기중입니다.")
serverSocket1 = socket(AF_INET, SOCK_STREAM)
serverSocket1.bind( (host, port+1))
serverSocket1.listen(1)
print("=== 1대기중입니다.")

connectionSocket, addr = serverSocket.accept()
print("{}에서 접속했습니다.".format(str(addr)))
connectionSocket1, addr1 = serverSocket1.accept()
print("{}에서 접속했습니다1.".format(str(addr1)))

sender = threading.Thread(target=send, args=(connectionSocket,))
receiver = threading.Thread(target=recv, args=(connectionSocket,))
sender1 = threading.Thread(target=send, args=(connectionSocket1,))
receiver1 = threading.Thread(target=recv, args=(connectionSocket1,))

sender.start()
receiver.start()
sender1.start()
receiver1.start()

'''
한 개의 접속만 유지하는 채팅 서버 프로그램
    - 간단, 
'''