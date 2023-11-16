from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import os
import zlib


def encrypt(message, public_key_bytes):
    # Load the public key from the transmitted bytes
    public_key = RSA.importKey(public_key_bytes)
    # Encrypt the message
    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(message)

    # Return as bytes
    return binascii.hexlify(ciphertext)

def decrypt(encrypted_message, private_key_bytes):
    # Load the private key from the transmitted bytes
    private_key = RSA.importKey(private_key_bytes)
    # Decompress the encrypted message
    compressed_ciphertext = binascii.unhexlify(encrypted_message)
    # Decrypt the message
    cipher = PKCS1_OAEP.new(private_key)
    plaintext = cipher.decrypt(compressed_ciphertext)
    return plaintext

# with open("keys/public_key.pem", "rb") as pub_file:
#     public_key = pub_file.read()

# with open("keys/private_key.pem", "rb") as prv_file:
#     private_key = prv_file.read()

# encrypted = encrypt("Drone-1", public_key)
# print(encrypted)
# decrypted = decrypt(encrypted, private_key)
# print(decrypted)
