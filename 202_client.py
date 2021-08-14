#!/usr/bin/env python3

from socket import *
import threading 

def send(sock):
    while True:
        sendData = input("")
        if sendData != 'exit':
            sock.send((nick+": "+sendData).encode("utf-8"))
        else:
            sock.close() 
def recv(sock):
    while True:
        data = sock.recv(1024)
        print(data.decode("utf-8"))

ip = str(input("IP: "))
port = 65432

nick=str(input("닉네임: "))
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect( (ip, port))
clientSocket.send(nick.encode('utf-8'))

print("접속완료")

sender = threading.Thread(target=send, args=(clientSocket, ))
receiver = threading.Thread(target=recv, args = (clientSocket,))

sender.start()
receiver.start()
