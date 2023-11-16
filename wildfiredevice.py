# -*- coding: utf-8 -*-

import time
import random
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


class WildfireMonitor:
    def __init__(self):
        # Initialize sensors and set threshold values
        self.smoke_particle_sensor = SmokeParticleSensor(threshold=30)
        self.infrared_sensor = InfraredSensor(threshold=0.2)
        self.gas_sensor = GasSensor(threshold=20)
        self.wind_sensor = WindSensor(threshold_speed=4)
        self.humidity_sensor = HumiditySensor(threshold=30)
        self.temperature_probe = TemperatureProbe(threshold=20)
        self.gps_tracker = GPSTracker()
        self.fire_radiometer = FireRadiometer(threshold=50)
        self.gps = (-35,-20)
        self.smoke_particle_sensor_active = 0
        self.infrared_sensor_active = 0
        self.gas_sensor_active = 0
        self.wind_sensor_active = 0
        self.humidity_sensor_active = 0
        self.temperature_probe_active = 0
        self.fire_radiometer_active = 0


    def read_sensors(self):
        while True:
            smoke_level = self.smoke_particle_sensor.detect_smoke()
            infrared_data = self.infrared_sensor.measure_infrared()
            gas_level = self.gas_sensor.detect_gas()
            wind_direction, wind_speed = self.wind_sensor.measure_wind()
            humidity_level = self.humidity_sensor.measure_humidity()
            temperature = self.temperature_probe.measure_temperature()
            fire_intensity = self.fire_radiometer.measure_fire_intensity()
            self.smoke_particle_sensor_active = smoke_level > self.smoke_particle_sensor.threshold
            self.infrared_sensor_active = infrared_data > self.infrared_sensor.threshold
            self.gas_sensor_active = gas_level > self.gas_sensor.threshold
            self.wind_sensor_active = wind_speed > self.wind_sensor.threshold_speed
            self.humidity_sensor_active = humidity_level < self.humidity_sensor.threshold
            self.temperature_probe_active = temperature > self.temperature_probe.threshold
            self.fire_radiometer_active = fire_intensity > self.fire_radiometer.threshold

            # Check if all values are above their thresholds
            above_threshold_count = sum([
                self.smoke_particle_sensor_active,
                self.infrared_sensor_active,
                self.gas_sensor_active,
                self.wind_sensor_active,
                self.humidity_sensor_active,
                self.temperature_probe_active,
                self.fire_radiometer_active
            ])
            if above_threshold_count >= 6:
                print("🔥 " + device_name + ": The sensors indicate a wildfire is happening ✅")
            else:
                print("🔥 " + device_name + ": The sensors indicate a wildfire is NOT happening ❌")
            time.sleep(1)


class SmokeParticleSensor:
    def __init__(self, threshold):
        self.threshold = threshold


    def detect_smoke(self):
        # Simulate smoke detection 
        return random.randint(0, 100)


class InfraredSensor:
    def __init__(self, threshold):
        self.threshold = threshold


    def measure_infrared(self):
        # Simulate infrared measurement
        return random.uniform(0, 1)


class GasSensor:
    def __init__(self, threshold):
        self.threshold = threshold


    def detect_gas(self):
        # Simulate gas detection 
        return random.randint(0, 50)


class WindSensor:
    def __init__(self, threshold_speed):
        self.threshold_speed = threshold_speed


    def measure_wind(self):
        # Simulate wind measurement 
        return random.randint(0, 360), random.uniform(0, 10)


class HumiditySensor:
    def __init__(self, threshold):
        self.threshold = threshold


    def measure_humidity(self):
        # Simulate humidity measurement 
        return random.uniform(0, 100)


class TemperatureProbe:
    def __init__(self, threshold):
        self.threshold = threshold


    def measure_temperature(self):
        # Simulate temperature measurement 
        return random.uniform(-10, 40)


class GPSTracker:
    def get_location(self):
        # Simulate GPS location 
        return (random.uniform(-90, 90), random.uniform(-180, 180))


class FireRadiometer:
    def __init__(self, threshold):
        self.threshold = threshold

    def measure_fire_intensity(self):
        # Simulate fire intensity measurement 
        return random.uniform(0, 100)
    

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
        time.sleep(1)


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
    data_response = "data"+"/"+str(interest_code)+"/"+str(requested_device)+"/"+str(getattr(fireMonitor, requested_data))
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
    global fireMonitor
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
    fireMonitor = WildfireMonitor()
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
    print("🔥 " + device_name + ": socket connected via UDP.")
    generate_data_thread = threading.Thread(target=fireMonitor.read_sensors)
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
