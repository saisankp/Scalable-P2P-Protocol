from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import zlib

# Function below by Prathamesh Sai
def generate_keys():
    # Generate a new RSA key pair
    key = RSA.generate(1024, e=65537)
    # Extract the public key
    public_key = key.publickey()
    # Export the pair of (private, public) keys in bytes
    private_key_in_bytes = key.exportKey()
    public_key_in_bytes = public_key.exportKey()
    return public_key_in_bytes, private_key_in_bytes


# Function below by Prathamesh Sai
def encrypt(message, public_key_bytes):
    # Load the public key from the transmitted bytes
    public_key = RSA.importKey(public_key_bytes)
    # Encrypt the message
    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(zlib.compress(message))
    # Return as bytes
    return binascii.hexlify(ciphertext)


# Function below by Prathamesh Sai
def decrypt(encrypted_message, private_key_bytes):
    # Load the private key from the transmitted bytes
    private_key = RSA.importKey(private_key_bytes)
    # Decompress the encrypted message
    compressed_ciphertext = binascii.unhexlify(encrypted_message)
    # Decrypt the message
    cipher = PKCS1_OAEP.new(private_key)
    plaintext = cipher.decrypt(compressed_ciphertext)
    return zlib.decompress(str(plaintext))
