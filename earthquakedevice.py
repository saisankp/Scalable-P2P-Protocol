# -*- coding: utf-8 -*-

import threading
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import socket
import threading
import re
import math
import os
import argparse
import subprocess
import signal


class Earthquake:
    def __init__(self):
        self.active = 0
        self.start = 0
        self.history = []


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
            if(bool(self.active)):
                print("🌋 " + device_name + ": The sensors indicate an earthquake is happening ✅")
            else:
                print("🌋 " + device_name + ": The sensors indicate an earthquake is NOT happening ❌")
            time.sleep(1)


class Seismometer:
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .5
        self.activated = 0


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
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .5
        self.activated = 0


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
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .5
        self.activated = 0


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
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .5
        self.activated = 0

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
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .5
        self.activated = 0


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
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .25
        self.activated = 0

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
    def __init__(self):
        self.output = 0
        self.history = []
        self.triggered = 0
        self.threshold = .5
        self.activated = 0

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
class DataMonitor:
    def __init__(self):
        self.history = []
        self.seismometer_active = 0
        self.accelerometer_active = 0
        self.inclinometer_active = 0
        self.acounsticsensor_active = 0
        self.straingauge_active = 0
        self.pwavesensor_active = 0
        self.swavesensor_active = 0
        self.gps = (50,50)

    def monitor_data(self):
        while True:
            time.sleep(1)
            self.seismometer_active = seismometer.activated
            self.accelerometer_active = accelerometer.activated
            self.inclinometer_active = inclinometer.activated
            self.acounsticsensor_active = acounsticsensor.activated
            self.straingauge_active = straingauge.activated
            self.pwavesensor_active = pwavesensor.activated
            self.swavesensor_active = swavesensor.activated


# Discover all other devices on the network
def discovery():
    while True:
        discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discovery_message = device_name
        try:
            # Check if port is available
            discovery_socket.bind((discovery_ip, discovery_port))
            discovery_socket.settimeout(1)
            connection_time = time.time()

            # Hold the connection for 5 seconds to listen for incoming discovery messages
            while time.time() - connection_time < 5:
                try:
                    data, sender_address = discovery_socket.recvfrom(1024)
                    knownDevices[data.decode()] = sender_address
                except socket.timeout:
                     print("🌋 " + device_name + ": Connected to 33333 and known devices to me are " + str(knownDevices).replace("u'", "'"))

            # Close socket to allow other devices to connect
            discovery_socket.close()
        except socket.error as e:
            # Send discovery message to the receiver
            device_socket.sendto(discovery_message.encode(), (discovery_ip, discovery_port))
        # Wait for 3 seconds before trying to discover more devices
        time.sleep(3)


# Send an interest packet for a piece of data on a different device
def send_interest_packet(data, device):
    global requestCodeNum
    requestCodeNum = requestCodeNum + 1
    requestCode = str(device_name)+str(requestCodeNum)
    packet = "interest"+"/"+requestCode+"/"+str(device)+"/"+str(data)
    interestRequests[requestCode] = [str(device), str(data)]
    # If no specific devices are mentioned in the call
    if device == "none":
        # Check if data is in the forwarding table
        if str(device)+"/"+str(data) in forwardingTable:
                device_socket.sendto(packet.encode(), forwardingTable[str(device)+"/"+str(data)])
        # If we have not seen this device before (from our forwarding table), perform flooding (contact all known devices)
        else:
            for devices in knownDevices:
                device_socket.sendto(packet.encode(), knownDevices[devices])
    else:
        device_socket.sendto(packet.encode(), knownDevices[device])
        time.sleep(.1)
        # Check if the requested data has been received
        if requestCode not in DataReceived:
            # If not, perform flooding (contact all known devices)
            print("No response from", device, "Performing flooding")
            for devices in knownDevices:
                device_socket.sendto(packet.encode(), knownDevices[devices])
            time.sleep(.1)
    return requestCode


# Handle an interest request coming from another device
def handle_interests(message, address):
    interest_code = message.split('/')[1]
    requested_device = message.split('/')[2]
    requested_data = message.split('/')[3]
    # If this is the requested device, send the info
    if requested_device == device_name:
        send_requested_data(message, address)

    # Otherwise, forward the packet if it hasnt been already
    elif interest_code not in interestForwards:
        interestForwards[interest_code] = address # add to list of unresolved interests
        # Check if requested data is in forwarding table
        if str(requested_device)+"/"+str(requested_data) in forwardingTable:
            print("🌋 " + device_name + ": Sending requested data from table")
            device_socket.sendto(message.encode(), forwardingTable[str(requested_device)+"/"+str(requested_data)])
        # If the requested data is not in the forwarding table, perform flooding (contact all known devices)
        else:
            for device in knownDevices:
                if knownDevices[device] != address: # Make sure to not send the interest back to the sender
                    device_socket.sendto(message.encode(), knownDevices[device])


# Handle data coming from a device
def handle_data(message, address):
    interest_code = message.split('/')[1]
    requested_device = message.split('/')[2]
    requested_data = message.split('/')[3]
    # Add sender to forwarding table
    forwardingTable[str(requested_device)+"/"+str(requested_data)] = address
    # If interest request was made by this device
    if interest_code in interestRequests:
        DataReceived[interest_code] = requested_data
        del interestRequests[interest_code]
    # If interest request was made by another device, forward to the correct device
    elif interest_code in interestForwards:
        device_socket.sendto(message.encode(), interestForwards[interest_code])
        del interestForwards[interest_code]
    # If the data has not been requested, perform flooding
    elif interest_code not in dataForwards:
        dataForwards[interest_code] = requested_data
        for device in knownDevices:
                if knownDevices[device] != address: # Make sure you don't send the interest back to the sender
                    device_socket.sendto(message.encode(), knownDevices[device])


# Send requested data to an address
def send_requested_data(message, address):
    interest_code = message.split('/')[1]
    requested_device = message.split('/')[2]
    requested_data = message.split('/')[3]
    # Package the data into a packet
    data_response = "data"+"/"+str(interest_code)+"/"+str(requested_device)+"/"+str(getattr(datamonitor, requested_data))
    device_socket.sendto(data_response.encode(), address)


# Recieve messages from other devices
def receive_messages():
    while True:
        try:
            # Wait until we receive a message through the socket
            data, sender_address = device_socket.recvfrom(1024)
            # Check if the message is an interest request or data
            if data.decode().split('/')[0] == "interest":
                handle_interests(data.decode(), sender_address)
            elif data.decode().split('/')[0] == "data":
                handle_data(data.decode(), sender_address)
        except socket.error as e: continue


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
    global earthquake
    global datamonitor
    global acounsticsensor
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
    global forwardingTable
    global interestForwards
    global interestRequests
    global dataForwards
    global DataReceived
    global requestCodeNum
    global device_socket

    # Initialise global variables
    earthquake = Earthquake()
    datamonitor = DataMonitor()
    acounsticsensor = AcousticSensor()
    inclinometer = Inclinometer()
    straingauge = StrainGauge()
    accelerometer = Accelerometer()
    seismometer = Seismometer()
    pwavesensor = PwaveSensor()
    swavesensor = SwaveSensor()
    device_name = arguments.device_name
    device_ip = arguments.device_ip
    device_port = arguments.device_port
    discovery_ip = arguments.discovery_ip
    discovery_port = arguments.discovery_port
    knownDevices = {} # Known devices are stored as device: (ip, port)
    forwardingTable = {} # In the format of address: device + "/" + data
    interestForwards = {} # In the format of interest code: address
    interestRequests = {} # Rrepresents the interest codes generated by this device
    dataForwards = {} # In the format of interest code: address
    DataReceived = {} # In the format of interest code: data
    requestCodeNum = 0 # Request codes are for packets when sending messages and having a unique ID for each
    device_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket for drone to communicate via UDP
    device_socket.bind((device_ip, device_port)) # Bind drone to specified unique port
    print("🌋 " + device_name + ": socket connected via UDP.")

    trigger_earthquake_thread = threading.Thread(target=earthquake.trigger_earthquake)
    seismometer_thread = threading.Thread(target=seismometer.generate_data)
    accelerometer_thread = threading.Thread(target=accelerometer.generate_data)
    inclinometer_thread = threading.Thread(target=inclinometer.generate_data)
    acounsticsensor_thread = threading.Thread(target=acounsticsensor.generate_data)
    straingauge_thread = threading.Thread(target=straingauge.generate_data)
    pwavesensor_thread = threading.Thread(target=pwavesensor.generate_data)
    swavesensor_thread = threading.Thread(target=swavesensor.generate_data)
    data_monitoring_thread = threading.Thread(target=datamonitor.monitor_data)
    discovery_thread = threading.Thread(target=discovery)
    receive_messages_thread = threading.Thread(target=receive_messages)

    trigger_earthquake_thread.start()
    seismometer_thread.start()
    accelerometer_thread.start()
    acounsticsensor_thread.start()
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
