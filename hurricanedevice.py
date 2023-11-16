# -*- coding: utf-8 -*-

import random
import time
import threading
import socket
import threading
import os
import signal
import subprocess
import argparse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

### sensor data
class HurricaneDevice:
    def __init__(self):
        # Sensor data and thresholds
        self.anemometer_data = 0
        self.barometer_data = 0
        self.hygrometer_data = 0
        self.thermometer_data = 0
        self.rain_gauge_data = 0
        self.lightning_detector_data = 0
        self.doppler_radar_data = 0
        self.storm_surge_sensor_data = 0
        self.anemometer_threshold = 85
        self.barometer_threshold = 1000
        self.hygrometer_threshold = 85
        self.thermometer_threshold = 32
        self.rain_gauge_threshold = 15
        self.lightning_detector_threshold = 8
        self.doppler_radar_threshold = 160
        self.storm_surge_sensor_threshold = 4
        self.gps = (-70,30)
        self.anemometer_active = 0
        self.barometer_active = 0
        self.hygrometer_active = 0
        self.thermometer_active = 0
        self.rain_gauge_active = 0
        self.lightning_detector_active = 0
        self.doppler_radar_active = 0
        self.storm_surge_sensor_active = 0


    def generate_sensor_data(self):
        while True:
            self.anemometer_data = random.uniform(0, 100)
            self.barometer_data = random.uniform(950, 1050)
            self.hygrometer_data = random.uniform(0, 100)
            self.thermometer_data = random.uniform(-10, 40)
            self.rain_gauge_data = random.uniform(0, 20)
            self.lightning_detector_data = random.randint(0, 10)
            self.doppler_radar_data = random.uniform(0, 200)
            self.storm_surge_sensor_data = random.uniform(0, 5)
            self.anemometer_active = self.anemometer_data > self.anemometer_threshold
            self.barometer_active = self.barometer_data < self.barometer_threshold
            self.hygrometer_active = self.hygrometer_data > self.hygrometer_threshold
            self.thermometer_active = self.thermometer_data > self.thermometer_threshold
            self.rain_gauge_active = self.rain_gauge_data > self.rain_gauge_threshold
            self.lightning_detector_active = self.lightning_detector_data > self.lightning_detector_threshold
            self.doppler_radar_active = self.doppler_radar_data > self.doppler_radar_threshold
            self.storm_surge_sensor_active = self.storm_surge_sensor_data > self.storm_surge_sensor_threshold
            
            # Check if all values are above their thresholds
            above_threshold_count = sum([
                self.anemometer_active,
                self.barometer_active,
                self.hygrometer_active,
                self.thermometer_active,
                self.rain_gauge_active,
                self.lightning_detector_active,
                self.doppler_radar_active,
                self.storm_surge_sensor_active
            ])
            if above_threshold_count >= 3:
                print("🌀 " + device_name + ": The sensors indicate a hurricane is happening ✅")
            else:
                print("🌀 " + device_name + ": The sensors indicate a hurricane is NOT happening ❌")
            time.sleep(2)


def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048,backend=default_backend())

    # Extract the public key
    public_key = private_key.public_key()

    # Serialize keys to PEM format
    private_key_str = private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption()).decode('utf-8')
    public_key_str = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')
    
    return public_key_str, private_key_str

def encrypt(message, public_key_str):
    # Load the public key from the transmitted string
    public_key_bytes = public_key_str.encode('utf-8')
    public_key = serialization.load_pem_public_key(public_key_bytes)

    # Encrypt the message
    ciphertext = public_key.encrypt(message.encode('utf-8'),padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

    return ciphertext.hex()

def decrypt(encrypted_message, private_key_str):
    # Load the private key from the transmitted string
    private_key_bytes = private_key_str.encode('utf-8')
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)

    # Decrypt the message
    plaintext = private_key.decrypt(
        bytes.fromhex(encrypted_message),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None)
    )

    return plaintext.decode('utf-8')


# Discover all other devices on the network
def discovery():
    while True:
        discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discovery_message = device_name+"/"+(public_key.replace("/", "_SLASH_"))
        for i in range(len(discovery_ip)): # add the 1 back in here
            device_socket.sendto(discovery_message.encode(), (discovery_ip[i], discovery_port))
        try:
            # Check if port is available
            discovery_socket.bind((discovery_ip[0], discovery_port))
            discovery_socket.settimeout(1)
            connection_time = time.time()

            # Hold the connection for 5 seconds to listen for incoming discovery messages
            while time.time() - connection_time < 2:
                try:
                    print("connected")
                    data, sender_address = discovery_socket.recvfrom(1024)
                    knownDevices[data.decode().split('/')[0]] = [sender_address, (data.decode().split('/')[1]).replace("_SLASH_", "/")]
                except socket.timeout:
                     print("🛸 " + device_name + ": Connected to 33333 and known devices to me are " + str(list(knownDevices.keys())).replace("u'", "'"))
            # Close socket to allow other devices to connect
            discovery_socket.close()
        except socket.error as e:
            # Send discovery message to the receiver
            device_socket.sendto(discovery_message.encode(), (discovery_ip[0], discovery_port))
        # Wait for 3 seconds before trying to discover more devices
        print("🛸 " + device_name + ": Known devices to me are " + str(list(knownDevices.keys())).replace("u'", "'"))
        time.sleep(2)


# Send an interest packet for a piece of data on a different device
def send_interest_packet(data, device):
    global requestCodeNum
    global DataReceived
    requestCodeNum = requestCodeNum + 1
    requestCode = str(device_name)+str(requestCodeNum)
    packet = "interest"+"/"+requestCode+"/"+str(device)+"/"+str(data)
    interestRequests[requestCode] = [str(device), str(data)]
    # If no specific devices are mentioned in the call
    if device == "none":
        # Check if data is in the forwarding table
        if str(device)+"/"+str(data) in forwardingTable:
                device_socket.sendto(encrypt(packet, knownDevices[device][1]).encode(), forwardingTable[str(device)+"/"+str(data)])
        # If we have not seen this device before (from our forwarding table), perform flooding (contact all known devices)
        else:
            for devices in knownDevices:
                device_socket.sendto(encrypt(packet, knownDevices[device][1]).encode(), knownDevices[devices][0])
    else:
        device_socket.sendto(encrypt(packet, knownDevices[device][1]).encode(), knownDevices[device][0])
        time.sleep(1)
        # Check if the requested data has been received
        if requestCode not in DataReceived:
            # If not, perform flooding (contact all known devices)
            print("No response from", device, "Performing flooding", requestCode)
            #for devices in knownDevices:
                #device_socket.sendto(encrypt(packet, knownDevices[device][1]).encode(), knownDevices[devices][0])
            time.sleep(1)
    return requestCode


# Handle an interest request coming from another device
def handle_interests(message, address):
    sender_name = get_sender_name(knownDevices,address[0],address[1])
    if sender_name != None:
        interest_code = message.split('/')[1]
        requested_device = message.split('/')[2]
        requested_data = message.split('/')[3]
        # If this is the requested device, send the info
        if requested_device == device_name:
            send_requested_data(message, address)

        # Otherwise, forward the packet if it hasnt been already
        elif interest_code not in interestForwards:
            print("Forwarding interest packet")
            interestForwards[interest_code] = sender_name # add to list of unresolved interests
            # Check if requested data is in forwarding table
            if str(requested_device)+"/"+str(requested_data) in forwardingTable:
                print("🛸 " + device_name + ": Sending requested data from table")
                device_socket.sendto(encrypt(message, knownDevices[sender_name][1]).encode(), forwardingTable[str(requested_device)+"/"+str(requested_data)])
            # If the requested data is not in the forwarding table, perform flooding (contact all known devices)
            else:
                for device in knownDevices:
                    if knownDevices[device][0] != address: # Make sure to not send the interest back to the sender
                        print("sending to device", knownDevices[device], knownDevices[device][0])
                        device_socket.sendto(encrypt(message, knownDevices[device][1]).encode(), knownDevices[device][0])


# Handle data coming from a device
def handle_data(message, address):
    sender_name = get_sender_name(knownDevices,address[0],address[1])
    if sender_name != None:
        interest_code = message.split('/')[1]
        requested_device = message.split('/')[2]
        requested_data = message.split('/')[3]
        # Add sender to forwarding table
        forwardingTable[str(requested_device)+"/"+str(requested_data)] = sender_name
        # If interest request was made by this device
        if interest_code in interestRequests:
            DataReceived[interest_code] = requested_data
            del interestRequests[interest_code]
        # If interest request was made by another device, forward to the correct device
        elif interest_code in interestForwards:
            device_socket.sendto(encrypt(message, knownDevices[interestForwards[interest_code]][1]).encode(), knownDevices[interestForwards[interest_code]][0])
            del interestForwards[interest_code]
        # If the data has not been requested, perform flooding
        elif interest_code not in dataForwards:
            dataForwards[interest_code] = requested_data
            for device in knownDevices:
                    if knownDevices[device] != address: # Make sure you don't send the interest back to the sender
                        device_socket.sendto(encrypt(message, knownDevices[sender_name][1]).encode(), knownDevices[device][0])


# Send requested data to an address
def send_requested_data(message, address):
    interest_code = message.split('/')[1]
    requested_device = message.split('/')[2]
    requested_data = message.split('/')[3]
    # Package the data into a packet
    data_response = "data"+"/"+str(interest_code)+"/"+str(requested_device)+"/"+str(getattr(hurricaneDevice, requested_data))
    sender_name = get_sender_name(knownDevices,address[0],address[1])
    if sender_name != None:
        device_socket.sendto(encrypt(data_response, knownDevices[sender_name][1]).encode(), address)


def get_sender_name(dictionary, target_ip, target_port):
    for sender_name, (address, key) in dictionary.items():
        if address[0] == target_ip and address[1] == target_port:
            return sender_name
    return None


# Recieve messages from other devices
def receive_messages():
    while True:
        try:
           # Wait until we receive a message through the socket
            data_encrypted, sender_address = device_socket.recvfrom(1024)
            # Check if sender is a known device
            sender = get_sender_name(knownDevices, sender_address[0], sender_address[1])
            if sender!= None:
                data_decrypted = decrypt(data_encrypted.decode(), private_key)

                # Check if the message is an interest request or data
                if data_decrypted.split('/')[0] == "interest":
                    handle_interests(data_decrypted, sender_address)
                elif data_decrypted.split('/')[0] == "data":
                    handle_data(data_decrypted, sender_address)
        except ConnectionResetError as e: continue


def parseArguments(parser):
    parser = argparse.ArgumentParser()
    argumentsAndDescriptions = {
        '--device-name': ('Name of device', str),
        '--device-ip': ('IP of device', str),
        '--device-port': ('Port of device', int),
        '--discovery-ip': ('IP for discovery', str),
        '--discovery-port': ('Port for discovery', int),
    }

    for argument, (description, argument_type) in argumentsAndDescriptions.items():
        parser.add_argument(argument, help=description, type=argument_type)

    arguments = parser.parse_args()

    for argument, (description, _) in argumentsAndDescriptions.items():
            if getattr(arguments, argument.replace("--", "").replace("-", "_")) is None:
                print("Error: Please specify {}".format(argument))
                exit(1)

    return arguments

def signal_handler(sig, frame):
    subprocess.check_output(['kill', '-9', str(os.getpid())])


def main():
    arguments = parseArguments(argparse.ArgumentParser())
    # Set the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Declare global variables
    global hurricaneDevice
    global device_name
    global device_ip
    global device_port
    global discovery_ip
    global discovery_port
    global knownDevices
    global forwardingTable
    global interestForwards
    global interestRequests
    global dataForwards
    global DataReceived
    global requestCodeNum
    global device_socket
    global public_key
    global private_key

    # Initialise global variables
    hurricaneDevice = HurricaneDevice()
    public_key, private_key =generate_keys()
    device_name = arguments.device_name
    device_ip = arguments.device_ip
    device_port = arguments.device_port
    discovery_ip = arguments.discovery_ip
    discovery_port = arguments.discovery_port
    knownDevices = {} # Known devices are stored as device: (ip, port), public key
    forwardingTable = {} # In the format of address: device + "/" + data
    interestForwards = {} # In the format of interest code: sender name
    interestRequests = {} # Rrepresents the interest codes generated by this device
    dataForwards = {} # In the format of interest code: sender name
    DataReceived = {} # In the format of interest code: data
    requestCodeNum = 0 # Request codes are for packets when sending messages and having a unique ID for each
    device_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket for drone to communicate via UDP
    device_socket.bind((device_ip, device_port)) # Bind drone to specified unique port
    print("🌀 " + device_name + ": socket connected via UDP.")
    generate_data_thread = threading.Thread(target=hurricaneDevice.generate_sensor_data)
    discovery_thread = threading.Thread(target=discovery)
    receive_messages_thread = threading.Thread(target=receive_messages)
    generate_data_thread.start()
    discovery_thread.start()
    receive_messages_thread.start()

    while True:
        # Keep running the main thread until the signal handler kills the process
        time.sleep(1)


if __name__ == "__main__":
    main()
