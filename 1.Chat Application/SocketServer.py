__author__ = 'vikas'

import socket

hostName = socket.gethostname() #server host name
portNumber = 8767 #server port number
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((hostName,portNumber))
s.listen(1)
(client,(h,p)) = s.accept()
print("Connected by ClientName=", client)
print("We got a connection from a client", (h,p))

while True:
    textFromServer=client.recv(1024)
    print(repr(textFromServer))
    print("Reply:")
    textToClient=input()
    client.send(textToClient.encode('utf-8'))

client.close()

