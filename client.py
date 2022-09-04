#Importing socket module
import socket
#Importing Encryption module
from encryption import Encryption
#Importing Thread for multithreading
from threading import Thread

#Client class
class Client:
    #Constructor
    def __init__(self, ip='127.0.0.1', port=55555):
        # Creating the encryption object
        self.encryption = Encryption()
        #Creating the socket object
        self.socket = socket.socket()
        #creating the address and port variable
        self.addr = (ip, port)
        # default disconnect callback
        # i.e. when server closes this method is called
        self.disconnectCallback = None
        # default message callback
        # i.e. when new message is received this method is called
        self.callback = None
        # default connected callback
        # i.e. when server connected this method is called
        self.connectedCallback = None
        #This is for denoting if the connection is active
        self.connected = False

    #Method to start the client socket
    def start(self):
        try:
            #Connecting to the server socket
            self.socket.connect(self.addr)

            #Local encryption key
            encryptionKey = self.encryption.getSerializedEncryptionKey()

            #Doing Handshake
            ##Getting the encryption of the server
            self.encryption.setSerializedEncryptionKey(self.recvall())
            ##Sending the encryption to the server
            self.socket.send(encryptionKey)

            #Calling the callback function for connected status
            self.connected = True
            self.callConnected()

            #Starting new thread for receiving message
            Thread(target=self.receive, args=(self.callback,)).start()

        except Exception as err:
            #Printing error message
            print(err)
            #Cloding the socket
            self.close()
            #Calling the disconnect callback method
            self.callDisconnect()
            return

    #Method for receiving the message from the server
    def receive(self, callback):
        while self.connected:
            try:
                message = self.recvall()
                #Decrypting the message
                decTxt = self.encryption.decrypt(message)
                #Calling the callback function for message
                callback(decTxt)
            except:
                #calling the disconnect callback method
                self.callDisconnect()
                break

    #Method to receive entire buffer from the socket
    def recvall(self):
        BUFF_SIZE = 1024 # 1 KiB
        data = b''
        while True:
            part = self.socket.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data

    #Method to set message receiving callback method
    def setOnMessage(self, callback):
        self.callback = callback

    #Method to set disconnected callback method
    def setOnDisconnect(self, callback):
        self.disconnectCallback = callback

    #Method to set connected callback method
    def setOnConnect(self, callback):
        self.connectedCallback = callback

    #Method to call disconnect callback method
    def callDisconnect(self):
        if self.disconnectCallback:
            self.disconnectCallback()
        self.close()

    #Method to call connect callback method
    def callConnected(self):
        if self.connectedCallback:
            self.connectedCallback()

    #Method to send the message to the server
    def send(self, message):
        #Encrypting the message
        encTxt = self.encryption.encrypt(message)
        #Sending the message to the server
        self.socket.send(encTxt)

    #Mthod to close the socket
    def close(self):
        self.connected = False
        self.socket.close()