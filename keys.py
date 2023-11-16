from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import binascii 

def generate_keys():
    # Generate a new RSA key pair
    key = RSA.generate(1024, e=65537)
    # Extract the public key
    public_key = key.publickey()
    if not os.path.exists("keys"):
        os.makedirs("keys")
    with open(os.path.join('keys', "private_key.pem"), "wb") as prv_file:
        prv_file.write(key.exportKey())
    with open(os.path.join('keys', "public_key.pem"), "wb") as pub_file:
        pub_file.write(public_key.exportKey())
    # Serialize keys to PEM format
    private_key_bytes = key.exportKey()
    public_key_bytes = public_key.exportKey()
    return public_key_bytes, private_key_bytes

generate_keys()