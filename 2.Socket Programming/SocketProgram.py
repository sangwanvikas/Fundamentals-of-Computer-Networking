__author__ = 'vikas'
#!/usr/bin/env python

import socket
import ssl
import math
import sys

try:
    class Client:
        __server_host_name = ''
        __port_number = 0
        __nu_id = ''
        __s = None
        __conn = None
        __message_to_server = ''
        __message_from_server = ''

        def __init__(self,portNumber,hostName,nuId,ssl_or_normal):
            self.__nu_id=nuId
            self.__server_host_name=hostName
            self.__port_number = portNumber
            self.__conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

            if ssl_or_normal == "NORMAL":
                self.createNormalSocket()
            elif ssl_or_normal == "SSL":
                self.createSSLSocket()

        def createNormalSocket(self):
            self.__conn.connect((self.__server_host_name, self.__port_number))
            self.sendHelloToServer()

        def createSSLSocket(self):
            self.__conn = ssl.wrap_socket(self.__conn, keyfile=None, certfile=None, server_side=False, cert_reqs=0,ssl_version=ssl.PROTOCOL_TLSv1,
                                  ca_certs=None, do_handshake_on_connect=True,suppress_ragged_eofs=False, ciphers=None)
            self.__conn.connect((self.__server_host_name, self.__port_number))
            self.sendHelloToServer()

        def sendHelloToServer(self):
            # send HELLO to server - 001901512 -001753883 -
            self.__message_to_server = "cs5700spring2015 HELLO " + self.__nu_id +"\n"
            self.__conn.send(self.__message_to_server)

            # receive STATUS from server ("cs5700spring2015 STATUS [a number] [a math operator] [another number]\n")
            self.__message_from_server = self.__conn.recv(1024)
            self.receiveStatusOrByeMessageFromServer()

        # perform CALCULATION
        def __performCalculation(self,status_message):
            list_status_message = status_message.split(' ')
            number_1 = int(list_status_message[2])
            operator = list_status_message[3]
            number_2 = int(list_status_message[4])
            result = 0
            if operator is '+':
                result = number_1 + number_2
            elif operator is '-':
                result = number_1 - number_2
            elif operator is '*':
                result = number_1 * number_2
            elif operator is '/':
                result = int(math.floor(number_1 / number_2))
            return result

        # send solution to the server and proceeds based on message from server (STATUS/BYE)
        # def stepsAfterCalculation(solution):
        def receiveStatusOrByeMessageFromServer(self):
            while True:
                solution = str(self.__performCalculation(self.__message_from_server))

                # send SOLUTION to the server ("cs5700spring2015 [the solution]\n")
                self.__message_to_server = "cs5700spring2015 " + solution + "\n"
                self.__conn.send(self.__message_to_server)
                # receives another STATUS or BYE from the server
                self.__message_from_server = self.__conn.recv(1024)

                # check this message and decide if calculation needs to be performed or not
                final_message_split = self.__message_from_server.split(' ')
                if len(final_message_split) is 5:
                    self.__performCalculation(self.__message_from_server)
                elif len(final_message_split) is 3:
                    print(final_message_split[1])
                    break
                else:
                    print("Neither returned STATUS message nor BYE message.")
                    break
except:
    print 'Error occured while communicating with the server!!'

try:
    # Code begins to instantiate object of Client
    defaultPortNumber = 27993
    SSLPortNumber = 27994
    portNumberFromUser = defaultPortNumber
    ssl_or_normal = "NORMAL"
    isCmdLineArgValid = True
    minusPFound = False
    minusSFound = False
    lastOptionalParamIndex = 0
    isCmdLineArgValid = True

    # Assign PortNumber and Socket type i.e. TCP/SSL
    for x in range(0,len(sys.argv)):
            if sys.argv[x] == "-p":
                portNumberFromUser = sys.argv[x+1]
                # check if -p occurs again
                if minusPFound is False and isinstance(int(portNumberFromUser),int) is True and (x == 1 or x == 2):
                    minusPFound = True
                else:
                    isCmdLineArgValid = False
                lastOptionalParamIndex = x+1

            if sys.argv[x] == "-s":
                ssl_or_normal = "SSL"
                # check -p not provided set default port number to 27994
                if minusPFound is False:
                    portNumberFromUser = 27994

                if minusSFound is False and (x == 1 or x == 3):
                    minusSFound = True
                else:
                    isCmdLineArgValid = False
                lastOptionalParamIndex = x

    # assign NUID and HostName
    nuIdFromUser = sys.argv[lastOptionalParamIndex+2]
    hostNameFromUser = sys.argv[lastOptionalParamIndex + 1]
    print (int(portNumberFromUser),hostNameFromUser,nuIdFromUser,ssl_or_normal)
    # Check if command line arguments are valid
    if lastOptionalParamIndex + 3 == len(sys.argv) and isCmdLineArgValid is True:
        Client(int(portNumberFromUser),hostNameFromUser,nuIdFromUser,ssl_or_normal)
    else:
        print "Error occured!! Please provide correct parameters and try again!!"

except:
    print "Error occured!! Please provide correct parameters and try again!!"

