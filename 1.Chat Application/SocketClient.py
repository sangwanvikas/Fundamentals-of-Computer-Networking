__author__ = 'vikas'
import socket

hostName = "127.0.1.1"
portNumber = 8767
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((hostName,portNumber))

while True:
    textToServer = input("Your Message :")
    msgFromClient = client_socket.send(textToServer.encode('utf-8'))
    print("Waiting for reply")

    textFromServer = client_socket.recv(1024)
    print("Received",repr(textFromServer))

client_socket.close()
