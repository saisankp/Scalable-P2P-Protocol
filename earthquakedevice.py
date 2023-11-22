# -*- coding: utf-8 -*-

import threading
import random
import time
import numpy as np
import socket
import threading
import re
import math
import os
import argparse
import subprocess
import signal
from cryptography import generate_keys, encrypt, decrypt


class Earthquake:
    # Function below by Sean Dowling
    def __init__(self):
        self.active = 0
        self.start = 0
        self.history = []


    # Function below by Sean Dowling
    def trigger_earthquake(self):
        i = 0
        while True:
            i = i + 1
            if self.active:
                if i - self.start > 20:
                    self.active = 0
            else:
                rand  = random.randrange(1, 60)
                if rand == 1 and i - self.start > 20:
                    self.start = i
                    self.active = 1
            self.history.append(self.active)
            time.sleep(1)


class Seismometer:
    # Function below by Sean Dowling
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .1
        self.activated = 0

    # Function below by Sean Dowling
    def generate_data(self):        
        high = 1
        low = .05
        amplitude = .1
        i = 0
        while True:
            i = i + 1
            noise = 0
            rand  = random.randrange(1, 4)
            if (not earthquake.active):
                if (rand == 1): # add some extra noise 
                    noise = random.uniform(-.1, .1)
                amplitude = amplitude - (amplitude - low)/100
                self.output = amplitude*np.sin(35*np.pi*i/1000) + noise
            else: 
                if (rand == 1): # add some extra noise 
                    noise = random.uniform(-.75, .75)
                amplitude = amplitude + (high - amplitude)/100
                self.output = amplitude*np.sin(35*np.pi*i/1000) + noise
            self.history.append(self.output)
            self.activated = abs(self.output) >= self.threshold
            time.sleep(1)


class Accelerometer:
    # Function below by Sean Dowling
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .5
        self.activated = 0


    # Function below by Sean Dowling
    def generate_data(self):
        while True:
            if (not earthquake.active): # random noise if there is no earthquake
                if abs(self.output) < (self.threshold*.9):
                    increment = random.uniform(-1.1*abs(self.output), .05)
                    rand  = random.randrange(1, 100)
                    if (rand == 1): # add some extra noise 
                        self.active = 1
                        increment = random.uniform(-1.6*abs(self.output), .2)

                elif abs(self.output) > (self.threshold*2):
                    increment = random.uniform(-.5, .1)

                else: increment = random.uniform(-.2, .1)

            else: # if there is an earthquake
                increment = random.uniform(-1.1*abs(self.output), .05)
                rand  = random.randrange(1, 4)
                if (rand == 1): # add some extra noise 
                    self.active = 1
                    increment = random.uniform(-1, .2)

            if self.output > 0: self.output = self.output + increment
            else: self.output = self.output - increment

            self.history.append(self.output)
            self.activated = abs(self.output) >= self.threshold
            time.sleep(1)


class Inclinometer:
    # Function below by Sean Dowling
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .5
        self.activated = 0


    # Function below by Sean Dowling
    def generate_data(self):
        while True:
            if (not earthquake.active): # random noise if there is no earthquake
                if abs(self.output) < (self.threshold*.9):
                    increment = random.uniform(-1.5*abs(self.output), .1)

                elif abs(self.output) > (self.threshold*2):
                    increment = random.uniform(-.5, .1)

                else: increment = random.uniform(-.2, .1)

            else: # if there is an earthquake
                if (abs(self.output) < (self.threshold*2)):
                    increment = random.uniform(-.2, .2)

                else: increment = random.uniform(-.2, .1)

            if self.output > 0: self.output = self.output + increment
            else: self.output = self.output - increment

            self.history.append(self.output)
            self.activated = abs(self.output) >= self.threshold
            time.sleep(1)


class StrainGauge:
    # Function below by Sean Dowling
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .5
        self.activated = 0


    # Function below by Sean Dowling
    def generate_data(self):
        high = .1
        amplitude = 0
        c = 0
        i = 0
        while True:
            i = i + 1
            noise = 0
            if (not earthquake.active):
                c = 0
                rand  = random.randrange(1, 40)
                if (rand == 1): # add some extra noise 
                    noise = random.uniform(0, .03)
                self.output = self.output-(self.output/50)+noise
            else:
                rand  = random.randrange(1, 5)
                if (rand == 1): # add some extra noise 
                    noise = random.uniform(-.2, .2)
                c = c + (.5-c)/100
                amplitude = amplitude + (high - amplitude)/10
                self.output = c+amplitude*np.sin(35*np.pi*i/1000) + noise
            self.history.append(self.output)
            self.activated = abs(self.output) >= self.threshold
            time.sleep(1)


class AcousticSensor:
    # Function below by Sean Dowling
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .5
        self.activated = 0

    # Function below by Sean Dowling
    def generate_data(self):
        while True:
            if (not earthquake.active): # random noise if there is no earthquake
                if (self.output < (self.threshold*.9)):
                    increment = random.uniform(max(-self.output, -.5*.5*self.threshold), .05)

                elif self.output > (self.threshold*2):
                    increment = random.uniform(max(-self.output, -3), 0)
                    
                elif self.output > (self.threshold):
                    increment = random.uniform(max(-self.output, -.2), 0)

                else: increment = random.uniform(0, .2)
            else: 
                if (self.output < (self.threshold)): # if there is an earthquake
                    increment = random.uniform(max(-self.output, -.25), .25)

                else: increment = random.uniform(max(-self.output, -.25), 0)
            self.output = self.output + increment
            self.history.append(self.output)
            self.activated = abs(self.output) >= self.threshold
            time.sleep(1)


class PwaveSensor:
    # Function below by Sean Dowling
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .25
        self.activated = 0


    # Function below by Sean Dowling
    def generate_data(self):        
        high = .5
        low = .05
        amplitude = .1
        i = 0
        while True:
            i = i + 1
            noise = 0
            rand  = random.randrange(1, 5)
            if (not earthquake.active):
                if (rand == 1): # add some extra noise 
                    noise = random.uniform(-.1, .1)
                amplitude = amplitude - (amplitude - low)/100
                self.output = amplitude*np.sin(35*np.pi*i/1000) + noise
            else: 
                if (rand == 1): # add some extra noise 
                    noise = random.uniform(-.5, .5)
                amplitude = amplitude + (high - amplitude)/10
                self.output = amplitude*np.sin(35*np.pi*i/1000) + noise
            self.history.append(self.output)
            self.activated = abs(self.output) >= self.threshold
            time.sleep(1)


class SwaveSensor:
    # Function below by Sean Dowling
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .5
        self.activated = 0


    # Function below by Sean Dowling
    def generate_data(self):        
        high = 1
        low = .1
        amplitude = .1
        i = 0
        while True:
            i = i + 1
            noise = 0
            rand  = random.randrange(1, 5)
            if (not earthquake.active):
                if (rand == 1): # add some extra noise 
                    noise = random.uniform(-.2, .2)
                amplitude = amplitude - (amplitude - low)/100
                self.output = amplitude*np.sin(35*np.pi*i/1000) + noise
            else: 
                if (rand == 1): # add some extra noise 
                    noise = random.uniform(-.75, .75)
                amplitude = amplitude + (high - amplitude)/100
                self.output = amplitude*np.sin(35*np.pi*i/1000) + noise
            self.history.append(self.output)
            self.activated = abs(self.output) >= self.threshold
            time.sleep(1)
            

# Checks if sensors are detecting an earthquake
class EarthquakeDevice:
    # Function below by Sean Dowling
    def __init__(self):
        self.history = []
        self.seismometer_active = 0
        self.accelerometer_active = 0
        self.inclinometer_active = 0
        self.acousticsensor_active = 0
        self.straingauge_active = 0
        self.pwavesensor_active = 0
        self.swavesensor_active = 0
        self.gps = (50,50)


    # Function below by Prathamesh Sai
    def monitor_data(self):
        while True:
            time.sleep(2)
            self.seismometer_active = seismometer.activated
            self.accelerometer_active = accelerometer.activated
            self.inclinometer_active = inclinometer.activated
            self.acousticsensor_active = acousticsensor.activated
            self.straingauge_active = straingauge.activated
            self.pwavesensor_active = pwavesensor.activated
            self.swavesensor_active = swavesensor.activated

            activated_sensors = [
            self.seismometer_active,
            self.accelerometer_active,
            self.inclinometer_active,
            self.acousticsensor_active,
            self.straingauge_active,
            self.pwavesensor_active,
            self.swavesensor_active
            ]

            # Device only sends sensor data to known devices
            if len(knownDevices) > 0:
                if(activated_sensors.count(True) >= 1):
                    print("🌋 " + device_name + ": The sensors indicate an earthquake is happening ✅")
                else:
                    print("🌋 " + device_name + ": The sensors indicate an earthquake is NOT happening ❌")


# Function below by Sean Downling (initial discovery networking + getting known devices) and Prathamesh Sai (getting public keys + discovering devices on various Raspberry Pi's and not only ours)
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
                    print("🌋 " + device_name + ": Connected to " + str(discovery_port) + " and my known devices are " + str(knownDevices).replace("u'", "'"))

            # Close socket to allow other devices to connect
            discovery_socket.close()
        except socket.error as e:
            device_socket.sendto(discovery_message+public_key, (discovery_ip[0], discovery_port))
                
        # Wait for 2 seconds before trying to discover more devices
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
            print("🌋 " + device_name + ": No response from " + device + ", performing flooding using my known devices! 🌊")
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
            print("🌋 " + device_name + ": Sending requested data from table")
            try:
                device_socket.sendto(encrypt(message, knownPublicKeys[str(forwardingTable[str(requested_device)+"/"+str(requested_data)])]), forwardingTable[str(requested_device)+"/"+str(requested_data)])
            except Exception:
                pass
        # If the requested data is not in the forwarding table, perform flooding (contact all known devices)
        else:
            for device in knownDevices:
                if knownDevices[device] != address: # Make sure to not send the interest back to the sender
                    try:
                        print("🌋 " + device_name + ": Forwarding packet to " + device)
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


# Function below by Sean Dowling
# Send requested data to an address
def send_requested_data(message, address):
    interest_code = decrypt(message, private_key).split('/')[1]
    requested_device = decrypt(message, private_key).split('/')[2]
    requested_data = decrypt(message, private_key).split('/')[3]
    # Package the data into a packet
    data_response = "data"+"/"+str(interest_code)+"/"+str(requested_device)+"/"+str(getattr(earthquakeDevice, requested_data))
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
                print("🌋 " + device_name + ": Waiting to discover device before responding back (public key needed)")
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
    global earthquake
    global earthquakeDevice
    global acousticsensor
    global inclinometer
    global straingauge
    global accelerometer
    global seismometer
    global pwavesensor
    global swavesensor
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
    earthquake = Earthquake()
    earthquakeDevice = EarthquakeDevice()
    acousticsensor = AcousticSensor()
    inclinometer = Inclinometer()
    straingauge = StrainGauge()
    accelerometer = Accelerometer()
    seismometer = Seismometer()
    pwavesensor = PwaveSensor()
    swavesensor = SwaveSensor()
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
    public_key, private_key = generate_keys() # Generate a pair of public and private keys specific for this earthquake device
    device_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket for drone to communicate via UDP
    device_socket.bind((device_ip, device_port)) # Bind drone to specified unique port
    print("🌋 " + device_name + ": socket connected via UDP.")

    trigger_earthquake_thread = threading.Thread(target=earthquake.trigger_earthquake)
    seismometer_thread = threading.Thread(target=seismometer.generate_data)
    accelerometer_thread = threading.Thread(target=accelerometer.generate_data)
    inclinometer_thread = threading.Thread(target=inclinometer.generate_data)
    acousticsensor_thread = threading.Thread(target=acousticsensor.generate_data)
    straingauge_thread = threading.Thread(target=straingauge.generate_data)
    pwavesensor_thread = threading.Thread(target=pwavesensor.generate_data)
    swavesensor_thread = threading.Thread(target=swavesensor.generate_data)
    data_monitoring_thread = threading.Thread(target=earthquakeDevice.monitor_data)
    discovery_thread = threading.Thread(target=discovery)
    receive_messages_thread = threading.Thread(target=receive_messages)

    trigger_earthquake_thread.start()
    seismometer_thread.start()
    accelerometer_thread.start()
    acousticsensor_thread.start()
    inclinometer_thread.start()
    straingauge_thread.start()
    pwavesensor_thread.start()
    swavesensor_thread.start()
    data_monitoring_thread.start()
    discovery_thread.start()
    receive_messages_thread.start()

    while True:
        # Keep running the main thread until the signal handler kills the process
        time.sleep(1)


if __name__ == "__main__":
    main()
