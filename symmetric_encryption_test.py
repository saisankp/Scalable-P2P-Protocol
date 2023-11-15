import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


device = "Charger"
device_name = "Charger-1"
device_ip = "localhost"
device_port = 33503
data = "GPS/(123,456)"

discovery_ip = "localhost"
discovery_port = 33333

# devices are stored as device: (ip, port)
knownDevices = {}
forwardingTable = {}  # device + "/" + data: address
interestForwards = {}  # interest code: address
interestRequests = []  # interest codes generated by this device
dataForwards = {}  # interest code: address
requestCode = 0


# Encryption key (Note: Replace this key with a more secure method of key management)
encryption_key = b'TestEncryptionKi'

def encrypt_data(key, plaintext):
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    tag = encryptor.tag
    return iv + tag + ciphertext

def decrypt_data(key, encrypted_data):
    iv = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()

plaintext = "/".join([str(device_name) + str(requestCode), str(device), str(data)])
discovery_message = str(device_name)+'/'+str(discovery_ip)+str(discovery_port)
interest_packet = 'interest'+'/'+plaintext
data_packet = 'data'+'/'+plaintext

discovery_message_encrypted=encrypt_data(encryption_key,discovery_message)
interest_packet_encrypted=encrypt_data(encryption_key,interest_packet)
data_packet_encrypted=encrypt_data(encryption_key,data_packet)

print("Discovery Message: ",discovery_message)
print("Discovery Message encrypted : ",discovery_message_encrypted)
print("Interest Packet : ",interest_packet )
print("Encrypted Interest Packet : ",interest_packet_encrypted)
print("Data Packet: ",data_packet)
print("Encrypted Data packet: ",data_packet_encrypted)

input_key=''
discovery_message_decrypted=''
interest_packet_decrypted=''
data_packet_decrypted=''

input_key = input('Enter key to decrypt discovery message: ')

# Ensure the input is exactly 16 characters
if len(input_key) != 16:
    print("Error: Please enter exactly 16 characters.")
    exit()

# Convert the input into a 16-byte key using UTF-8 encoding
input_key = input_key.encode('utf-8')

if input_key == encryption_key:
    discovery_message_decrypted = decrypt_data(input_key, discovery_message_encrypted)
    interest_packet_decrypted = decrypt_data(input_key, interest_packet_encrypted)
    data_packet_decrypted = decrypt_data(input_key, data_packet_encrypted)
    print("Discovery Message Decrypted: ", discovery_message_decrypted)
    print("Decrypted Interest Packet: ", interest_packet_decrypted)
    print("Decrypted Data packet: ", data_packet_decrypted)
else:
    print("Not the correct key")

