#Importing base64 for encoding and decoding of base64
import base64
#Importing all RSA modules from the cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

#Encryption Class
class Encryption:
    #Constructor
    def __init__(self):
        #setting class attributes
        #Generating new Keys
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        #Setting keys
        self.setKeys(public_key, private_key)
    
    #method to set private key or key for the decryption
    def setDecryptionKey(self, decryptionKey):
        self.decryptionKey = decryptionKey

    #method to set public key or key for the encryption
    def setEncryptionKey(self, encryptionKey):
        self.encryptionKey = encryptionKey

    #method to set public key or key for the encryption of this object
    def setMyEncryptionKey(self, encryptionKey):
        self.myEncryptionKey = encryptionKey

    #Set Both Encryption and Decryption keys simultaneously
    def setKeys(self, public_key, private_key):
        self.setMyEncryptionKey(public_key)
        self.setEncryptionKey(public_key)
        self.setDecryptionKey(private_key)

    #method to get public key or key for the encryption
    def getEncryptionKey(self):
        return self.encryptionKey

    #method to get public key or key for the encryption of this object
    def getMyEncryptionKey(self):
        return self.myEncryptionKey

    #method to get private key or key for the decryption
    def getDecryptionKey(self):
        return self.decryptionKey

    #method to set pickled public key or key for the encryption
    def setSerializedEncryptionKey(self, encryptionKey):
        #Unserialization the encryption key
        unserializedEncryptionKey = serialization.load_pem_public_key(
            encryptionKey,
            backend=default_backend()
        )
        self.setEncryptionKey(unserializedEncryptionKey)

    #method to get pickled public key or key for the encryption
    def getSerializedEncryptionKey(self):
        #Serialization
        serializedEncryptionKey = self.encryptionKey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return serializedEncryptionKey

    #Method to encrypt the text with public key or encryption key
    def encrypt(self, text):
        try:
            return base64.b64encode(self.encryptionKey.encrypt(
                text.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            ))
        except Exception as err:
            return text.encode()

    #Method to decrypt the encrypted text with private key or decryption key
    def decrypt(self, encText):
        try:
            return self.decryptionKey.decrypt(
                base64.b64decode(encText),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            ).decode()
        except:
            return encText