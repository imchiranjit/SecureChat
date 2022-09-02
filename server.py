import socket
import rsa
import pickle
from threading import Thread

class Server:
    def __init__(self, ip='', port=55555, maxuser=1):
        # generate public and private keys with
        # rsa.newkeys method,this method accepts
        # key length as its parameter
        # key length should be atleast 16
        self.publicKey, self.privateKey = rsa.newkeys(512)
        self.socket = socket.socket()
        self.client = None
        self.ip = ip
        self.port = port
        self.maxuser = maxuser
        self.socket.bind((self.ip, self.port))
        self.open = True

    def start(self):
        self.socket.listen(self.maxuser)
        while self.open:
            # Establish connection with client.
            client, addr = self.socket.accept()   
            self.client = client
            print ('Got connection from', addr )
            
            try:
                client.send(pickle.dumps(self.publicKey))
                self.clientPublicKey = pickle.loads(client.recv(1024))

                Thread(target=self.receive, args=(self.callback,)).start()

            except Exception as err:
                # Close the connection with the client
                client.close()
                print(err)
        self.socket.close()

    def printMessage(self, message):
        print(f"Message Received: {message}")

    #Method to encrypt the message
    def encrypt(self, txt):
        try:
            return rsa.encrypt(txt.encode(), self.clientPublicKey)
        except:
            return txt.encode()

    #Method to decrypt the encrypted message
    def decrypt(self, encTxt):
        try:
            return rsa.decrypt(encTxt, self.privateKey).decode()
        except:
            return encTxt

    def receive(self, callback):
        while self.open:
            try:
                message = self.client.recv(1024)
                decTxt = self.decrypt(message)
                callback(decTxt)
            except Exception as err:
                print(err)
                break

    def setOnMessage(self, callback):
        self.callback = callback

    def send(self, message):
        encTxt = self.encrypt(message)
        self.client.send(encTxt)

    def close(self):
        self.open = False
        if self.client:
            self.client.close()
        # self.socket.close()

