from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os

KEYS_DIRECTORY = "keys"
PRIVATE_KEY_FILENAME = "private_key.pem"
PUBLIC_KEY_FILENAME = "public_key.pem"

def generate_keys():
    # Generate a new RSA key pair
    key = RSA.generate(1024, e=65537)
    # Extract the public key
    public_key = key.publickey()
    if not os.path.exists("keys"):
        os.makedirs("keys")
    with open(os.path.join(KEYS_DIRECTORY, PRIVATE_KEY_FILENAME), "wb") as prv_file:
        prv_file.write(key.exportKey())
    with open(os.path.join(KEYS_DIRECTORY, PUBLIC_KEY_FILENAME), "wb") as pub_file:
        pub_file.write(public_key.exportKey())
    # Serialize keys to PEM format
    private_key_bytes = key.exportKey()
    public_key_bytes = public_key.exportKey()
    return public_key_bytes, private_key_bytes