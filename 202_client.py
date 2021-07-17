#!/usr/bin/env python3

from socket import *
import threading 

def send(sock):
    while True:
        sendData = input(">>> ")
        if sendData != 'quit':
            sock.send(sendData.encode("utf-8"))
        else:
            sock.close() 
def recv(sock):
    while True:
        data = sock.recv(1024)
        print("\n상대방:", data.decode("utf-8"))
        print(">>> ")

ip = "127.0.0.1"
port = 65432

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket1 = socket(AF_INET, SOCK_STREAM)
clientSocket.connect( (ip, port))
clientSocket1.connect( (ip, port+1))

print("접속완료")

sender = threading.Thread(target=send, args=(clientSocket,))
sender = threading.Thread(target=send, args=(clientSocket1,))
receiver = threading.Thread(target=recv, args = (clientSocket,))
receiver = threading.Thread(target=recv, args = (clientSocket1,))

sender.start()
receiver.start()

'''
초간단, 쓰레드를 이용한 채팅 클라이언트 
'''