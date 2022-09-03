#Importing socket module
import socket
#Importing Encryption module
from encryption import Encryption
#Importing Thread for multithreading
from threading import Thread

#Server Class
class Server:
    def __init__(self, ip='', port=55555, maxuser=1):
        # Creating the encryption object
        self.encryption = Encryption()
        #Creating the socket object
        self.socket = socket.socket()
        #creating the client variable
        self.client = None
        #Creating the address and port tuple
        self.addr = (ip, port)
        #Creating max waiting client variable
        self.maxuser = maxuser
        #Binding the address to the socket
        self.socket.bind(self.addr)
        #Variable to denote connection status
        self.open = True

        # default connected callback
        # i.e. when server connected this method is called
        self.connectedCallback = None

    #Method to start the server socket
    def start(self):

        #Start listening for the client connection
        self.socket.listen(self.maxuser)

        while self.open:
            # Establish connection with client.
            client, addr = self.socket.accept()
            #Setting client variable 
            self.client = client
            print ('Got connection from', addr )
            
            try:

                #Doing Handshake
                ##Sending the encryption to the client
                client.send(self.encryption.getPickledEncryptionKey())
                ##Getting the encryption of the client
                self.encryption.setPickledEncryptionKey(client.recv(1024))

                #Starting new thread for receiving message
                Thread(target=self.receive, args=(self.callback,)).start()

                #Calling the callback function for connected status
                self.callConnected()

            except Exception as err:
                # Close the connection with the client
                client.close()
                #Printin the connection
                print(err)

        #Closing the socket connection
        # self.socket.close()

    #Method for receiving the message from the server
    def receive(self, callback):
        while self.open:
            try:
                message = self.client.recv(1024)
                #Decrypting the message
                decTxt = self.encryption.decrypt(message)
                #Calling the callback function for message
                callback(decTxt)
            except:
                #calling the disconnect callback method
                self.callDisconnect()
                #Printing the error message
                break

    # def receive(self, callback):
    #     while self.open:
    #         try:
    #             message = self.client.recv(1024)
    #             decTxt = self.decrypt(message)
    #             callback(decTxt)
    #         except Exception as err:
    #             self.callDisconnect()
    #             print(err)
    #             break

    #Method to set message receiving callback method
    def setOnMessage(self, callback):
        self.callback = callback

    #Method to call connect callback method
    def callConnected(self):
        if self.connectedCallback:
            self.connectedCallback()

    #Method to set connected callback method
    def setOnConnect(self, callback):
        self.connectedCallback = callback

    #Method to call disconnect callback method
    def callDisconnect(self):
        if self.disconnectCallback:
            self.disconnectCallback()

    #Method to set disconnected callback method
    def setOnDisconnect(self, callback):
        self.disconnectCallback = callback

    #Method to send the message to the client
    def send(self, message):
        #Encrypting the message
        encTxt = self.encryption.encrypt(message)
        #Sending the message to the client
        self.client.send(encTxt)

    #Closing the socket connection
    def close(self):
        self.open = False
        if self.client:
            self.client.close()
        # self.socket.close()

