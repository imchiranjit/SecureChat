#Importing RSA module
import rsa
#Importig pickle module for sending objects through the socket
import pickle

#Encryption Class
class Encryption:
    #Constructor
    def __init__(self):
        #setting class attributes
        #Generating new Keys
        self.setKeys(rsa.newkeys(512))
    
    #method to set private key or key for the decryption
    def setDecryptionKey(self, decryptionKey):
        self.decryptionKey = decryptionKey

    #method to set public key or key for the encryption
    def setEncryptionKey(self, encryptionKey):
        self.encryptionKey = encryptionKey

    #Set Both Encryption and Decryption keys simultaneously
    def setKeys(self, keys):
        self.setEncryptionKey(keys[0])
        self.setDecryptionKey(keys[1])

    #method to get public key or key for the encryption
    def getEncryptionKey(self):
        return self.encryptionKey

    #method to get private key or key for the decryption
    def getDecryptionKey(self):
        return self.decryptionKey

    #method to set pickled public key or key for the encryption
    def setPickledEncryptionKey(self, encryptionKey):
        #Unpicklling the encryption key
        unpickledEncryptionKey = pickle.loads(encryptionKey)
        self.setEncryptionKey(unpickledEncryptionKey)

    #method to get pickled public key or key for the encryption
    def getPickledEncryptionKey(self):
        #Picklling
        pickledEncryptionKey = pickle.dumps(self.getEncryptionKey())
        return pickledEncryptionKey

    #Method to encrypt the text with public key or encryption key
    def encrypt(self, text):
        try:
            return rsa.encrypt(text.encode(), self.encryptionKey)
        except Exception as err:
            return text.encode()

    #Method to decrypt the encrypted text with private key or decryption key
    def decrypt(self, encText):
        try:
            return rsa.decrypt(encText, self.decryptionKey).decode()
        except:
            return encText