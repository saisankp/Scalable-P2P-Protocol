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
    ciphertext = cipher.encrypt(zlib.compress(message))

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
    # print(plaintext)
    return zlib.decompress(str(plaintext))

with open("keys/public_key.pem", "rb") as pub_file:
    public_key = pub_file.read()

with open("keys/private_key.pem", "rb") as prv_file:
    private_key = prv_file.read()

# encrypted = encrypt("Drone-1", public_key)
# print(encrypted)
# decrypted = decrypt("3ef22d1aaebe9aed6da76ee7c7ffb8a7c3f0d3c4e81c1f773aa0ff0b7b7fd86a22a761e97881d91fb01da288cc9eb9d17e4b5c4388b9c7d81d4f11e89c3dd06c020d66d7ce54d92f5aaba8b21cefa9ad14121644a90ef64efa0794126193e8dd57db6395fd122376de2b6753f1a8089527052b5cade176b2e99c28fc93636b24", private_key)
# print(decrypted)