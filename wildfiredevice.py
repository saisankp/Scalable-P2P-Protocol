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
from cryptography import generate_keys, encrypt, decrypt


class WildfireDevice:
    # Function below by Hamzah Khan
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
        
    
    # Function below by Prathamesh Sai
    def read_sensors(self):
        while True:
            time.sleep(2)
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

            # Device only sends sensor data to known devices
            if len(knownDevices) > 0:
                if above_threshold_count >= 6:
                    print("🔥 " + device_name + ": The sensors indicate a wildfire is happening ✅")
                else:
                    print("🔥 " + device_name + ": The sensors indicate a wildfire is NOT happening ❌")


class SmokeParticleSensor:
    # Function below by Hamzah Khan
    def __init__(self, threshold):
        self.threshold = threshold


    # Function below by Hamzah Khan
    def detect_smoke(self):
        # Simulate smoke detection 
        return random.randint(0, 100)


class InfraredSensor:
    # Function below by Hamzah Khan
    def __init__(self, threshold):
        self.threshold = threshold


    # Function below by Hamzah Khan
    def measure_infrared(self):
        # Simulate infrared measurement
        return random.uniform(0, 1)


class GasSensor:
    # Function below by Hamzah Khan
    def __init__(self, threshold):
        self.threshold = threshold


    # Function below by Hamzah Khan
    def detect_gas(self):
        # Simulate gas detection 
        return random.randint(0, 50)


class WindSensor:
    # Function below by Hamzah Khan
    def __init__(self, threshold_speed):
        self.threshold_speed = threshold_speed


    # Function below by Hamzah Khan
    def measure_wind(self):
        # Simulate wind measurement 
        return random.randint(0, 360), random.uniform(0, 10)


class HumiditySensor:
    # Function below by Hamzah Khan
    def __init__(self, threshold):
        self.threshold = threshold


    # Function below by Hamzah Khan
    def measure_humidity(self):
        # Simulate humidity measurement 
        return random.uniform(0, 100)


class TemperatureProbe:
    # Function below by Hamzah Khan
    def __init__(self, threshold):
        self.threshold = threshold


    # Function below by Hamzah Khan
    def measure_temperature(self):
        # Simulate temperature measurement 
        return random.uniform(-10, 40)


class GPSTracker:
    # Function below by Hamzah Khan
    def get_location(self):
        # Simulate GPS location 
        return (random.uniform(-90, 90), random.uniform(-180, 180))


class FireRadiometer:
    # Function below by Hamzah Khan
    def __init__(self, threshold):
        self.threshold = threshold

    # Function below by Hamzah Khan
    def measure_fire_intensity(self):
        # Simulate fire intensity measurement 
        return random.uniform(0, 100)
    

# Function below by Sean Dowling
# Discover all other devices in the network
def discovery():        
    while True:
        discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discovery_message = device_name
        for ip in range(1, len(discovery_ip)):
            # Add our public key to the discovery message so other devices can communicate to us
            device_socket.sendto(discovery_message+public_key, (discovery_ip[ip], discovery_port))
        try:
            # Check if port is available
            discovery_socket.bind((discovery_ip[0], discovery_port))
            discovery_socket.settimeout(1)
            connection_time = time.time()

            # Hold the connection for 5 seconds to listen for incoming discovery messages
            while time.time() - connection_time < 5:
                try:
                    data, sender_address = discovery_socket.recvfrom(1024)
                    # Extract the name of the device and its public key from discovery
                    begin_index = data.find("-----BEGIN PUBLIC KEY-----")
                    discovery_device_name = data[:begin_index].strip()
                    discovery_device_public_key = data[begin_index:].strip()
                    # Keep a dictionary of known devices from discovery
                    knownDevices[discovery_device_name] = sender_address
                    # Keep a dictionary of public keys for when we send messages to our known devices
                    knownPublicKeys[str(sender_address)] = discovery_device_public_key
                except socket.timeout:
                    print("🔥 " + device_name + ": Connected to " + str(discovery_port) + " and my known devices are " + str(knownDevices).replace("u'", "'"))

            # Close socket to allow other devices to connect
            discovery_socket.close()
        except socket.error as e:
            device_socket.sendto(discovery_message+public_key, (discovery_ip[0], discovery_port))
                
        # Wait for 1 seconds before trying to discover more devices
        time.sleep(2)


# Function below by Sean Dowling
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
                device_socket.sendto(encrypt(packet, knownPublicKeys[str(forwardingTable[str(device)+"/"+str(data)])]), forwardingTable[str(device)+"/"+str(data)])
        # If we have not seen this device before (from our forwarding table), perform flooding (contact all known devices)
        else:
            for devices in knownDevices:
                device_socket.sendto(encrypt(packet, knownPublicKeys[str(knownDevices[devices])]), knownDevices[devices])
    else:
        device_socket.sendto(encrypt(packet, knownPublicKeys[str(knownDevices[device])]), knownDevices[device])
        time.sleep(0.1)
        # Check if the requested data has been received
        if requestCode not in str(DataReceived) and len([key for key in forwardingTable if key.startswith(device+"/")]) > 0:
            # If not, perform flooding (contact all known devices)
            print("🔥 " + device_name + ": No response from " + device + ", performing flooding using my known devices! 🌊")
            for devices in knownDevices:
                device_socket.sendto(encrypt(packet, knownPublicKeys[str(knownDevices[devices])]), knownDevices[devices])
            time.sleep(0.1)
    time.sleep(0.2)
    return requestCode


# Function below by Sean Dowling
# Handle an interest request coming from another device
def handle_interests(message, address):
    interest_code = decrypt(message, private_key).split('/')[1]
    requested_device = decrypt(message, private_key).split('/')[2]
    requested_data = decrypt(message, private_key).split('/')[3]
    
    # If this is the requested device, send the info
    if requested_device == device_name:
        send_requested_data(message, address)

    # Otherwise, forward the packet if it hasnt been already
    elif interest_code not in interestForwards:
        interestForwards[interest_code] = address # add to list of unresolved interests
        # Check if requested data is in forwarding table
        if str(requested_device)+"/"+str(requested_data) in forwardingTable:
            print("🔥 " + device_name + ": Sending requested data from table")
            try:
                device_socket.sendto(encrypt(message, knownPublicKeys[str(forwardingTable[str(requested_device)+"/"+str(requested_data)])]), forwardingTable[str(requested_device)+"/"+str(requested_data)])
            except Exception:
                pass
        # If the requested data is not in the forwarding table, perform flooding (contact all known devices)
        else:
            for device in knownDevices:
                if knownDevices[device] != address: # Make sure to not send the interest back to the sender
                    try:
                        print("🔥 " + device_name + ": Forwarding packet to " + device)
                        device_socket.sendto(encrypt(decrypt(message, private_key), knownPublicKeys[str(knownDevices[device])]), knownDevices[device])
                    except Exception as e:
                        continue


# Function below by Sean Dowling
# Handle data coming from a device
def handle_data(message, address):
    interest_code = decrypt(message, private_key).split('/')[1]
    requested_device = decrypt(message, private_key).split('/')[2]
    requested_data = decrypt(message, private_key).split('/')[3]
    # Add sender to forwarding table
    forwardingTable[str(requested_device)+"/"+str(requested_data)] = address
    # If interest request was made by this device
    if interest_code in interestRequests:
        DataReceived[interest_code] = requested_data
        del interestRequests[interest_code]
    # If interest request was made by another device, forward to the correct device
    elif interest_code in interestForwards:
        device_socket.sendto(encrypt(decrypt(message, private_key), knownPublicKeys[str(interestForwards[interest_code])]), interestForwards[interest_code])
        del interestForwards[interest_code]
    # If the data has not been requested, perform flooding
    elif interest_code not in dataForwards:
        dataForwards[interest_code] = requested_data
        for device in knownDevices:
                if knownDevices[device] != address: # Make sure you don't send the interest back to the sender
                    device_socket.sendto(encrypt(decrypt(message, private_key), knownPublicKeys[str(knownDevices[device])]), knownDevices[device])
                    # device_socket.sendto(message, knownDevices[device])


# Function below by Sean Dowling
# Send requested data to an address
def send_requested_data(message, address):
    interest_code = decrypt(message, private_key).split('/')[1]
    requested_device = decrypt(message, private_key).split('/')[2]
    requested_data = decrypt(message, private_key).split('/')[3]
    # Package the data into a packet
    data_response = "data"+"/"+str(interest_code)+"/"+str(requested_device)+"/"+str(getattr(wildfireDevice, requested_data))
    device_socket.sendto(encrypt(data_response, knownPublicKeys[str(address)]), address)


# Function below by Prathamesh Sai
# Recieve messages from other devices
def receive_messages():
    while True:
        try:
            # Wait until we receive a message through the socket
            data, sender_address = device_socket.recvfrom(1024)
            if str(sender_address) in knownPublicKeys:
                # Check if the message is an interest request or data
                try:
                    decrypted_data = decrypt(data, private_key)
                    if decrypted_data.split('/')[0] == "interest":
                        handle_interests(data, sender_address)
                    elif decrypted_data.split('/')[0] == "data":
                        handle_data(data, sender_address)
                except Exception as e: continue
            else:
                print("🔥 " + device_name + ": Waiting to discover device before responding back (public key needed)")
        except socket.error: 
            continue


# Function below by Prathamesh Sai
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
        parser.add_argument(argument, nargs='+', help=description, type=argument_type)

    arguments = parser.parse_args()

    for argument, (description, _) in argumentsAndDescriptions.items():
            if getattr(arguments, argument.replace("--", "").replace("-", "_")) is None:
                print("Error: Please specify {}".format(argument))
                exit(1)

    return arguments


# Function below by Prathamesh Sai
def signal_handler(sig, frame):
    subprocess.check_output(['kill', '-9', str(os.getpid())])


# Function below by Prathamesh Sai
def main():
    arguments = parseArguments(argparse.ArgumentParser())
    # Set the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Declare global variables
    global wildfireDevice
    global device_name
    global device_ip
    global device_port
    global discovery_ip
    global discovery_port
    global knownDevices
    global knownPublicKeys
    global forwardingTable
    global interestForwards
    global interestRequests
    global dataForwards
    global DataReceived
    global requestCodeNum
    global public_key
    global private_key
    global device_socket

    # Initialise global variables
    wildfireDevice = WildfireDevice()
    device_name = arguments.device_name[0]
    device_ip = arguments.device_ip[0]
    device_port = arguments.device_port[0]
    discovery_ip = arguments.discovery_ip
    discovery_port = arguments.discovery_port[0]
    knownDevices = {} # Known devices are stored as device: (ip, port)
    knownPublicKeys = {} # Known public keys are stored and differentiated with the (ip, port) where they come from
    forwardingTable = {} # In the format of address: device + "/" + data
    interestForwards = {} # In the format of interest code: address
    interestRequests = {} # Rrepresents the interest codes generated by this device
    dataForwards = {} # In the format of interest code: address
    DataReceived = {} # In the format of interest code: data
    requestCodeNum = 0 # Request codes are for packets when sending messages and having a unique ID for each
    public_key, private_key = generate_keys() # Generate a pair of public and private keys specific for this wildfire device
    device_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket for drone to communicate via UDP
    device_socket.bind((device_ip, device_port)) # Bind drone to specified unique port
    print("🔥 " + device_name + ": socket connected via UDP.")
    generate_data_thread = threading.Thread(target=wildfireDevice.read_sensors)
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