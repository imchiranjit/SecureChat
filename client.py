import socket
import rsa
import pickle
from threading import Thread

class Client:
    def __init__(self, ip='127.0.0.1', port=55555):
        # generate public and private keys with
        # rsa.newkeys method,this method accepts
        # key length as its parameter
        # key length should be atleast 16
        self.publicKey, self.privateKey = rsa.newkeys(512)
        self.socket = socket.socket()
        self.addr = (ip, port)
        self.disconnectCallback = None
        self.callback = None
        self.connectedCallback = None
        self.connected = False

    def start(self):
        try:
            self.socket.connect(self.addr)

            self.serverPublicKey = pickle.loads(self.socket.recv(1024))
            self.socket.send(pickle.dumps(self.publicKey))

            self.connected = True
            self.callConnected()

            Thread(target=self.receive, args=(self.callback,)).start()

        except Exception as err:
            print(err)
            self.close()
            self.callDisconnect()
            return


    #Method to encrypt the message
    def encrypt(self, txt):
        try:
            return rsa.encrypt(txt.encode(), self.serverPublicKey)
        except Exception as err:
            return txt.encode()

    #Method to decrypt the encrypted message
    def decrypt(self, encTxt):
        try:
            return rsa.decrypt(encTxt, self.privateKey).decode()
        except:
            return encTxt

    def receive(self, callback):
        while self.connected:
            try:
                message = self.socket.recv(1024)
                decTxt = self.decrypt(message)
                callback(decTxt)
            except:
                self.callDisconnect()
                break

    def setOnMessage(self, callback):
        self.callback = callback

    def setOnDisconnect(self, callback):
        self.disconnectCallback = callback

    def setOnConnect(self, callback):
        self.connectedCallback = callback

    def callDisconnect(self):
        if self.disconnectCallback:
            self.disconnectCallback()
        self.close()

    def callConnected(self):
        if self.connectedCallback:
            self.connectedCallback()

    def send(self, message):
        encTxt = self.encrypt(message)
        self.socket.send(encTxt)

    def close(self):
        self.connected = False
        self.socket.close()