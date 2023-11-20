# -*- coding: utf-8 -*-

import time
import socket
import os
import threading
import re
import math
import signal
import subprocess
import argparse
from cryptography import generate_keys, encrypt, decrypt


class DroneCharger:
    def __init__(self):
        self.gps = (60,-2) # Latitude, Longitude
        self.voltage = 0 # Volts
        self.power = 0 # Watts
        self.temperature = 20 # Degrees celcius
        self.solar_power_charging_rate = 0 # Watt hour (Wh/m) 
        self.usage_status = False # If the drone charger is being used
        self.locking_actuator_status = False # If the locking actuator that locks a drone onto the charger is open or closed
        self.fire_alarm_sensor = False # If the fire alarm on the charger is triggered or not


    # GPS does not change unless it is being transported
    # Temperature does not change unless there is a fire/stress on power
    # Usage status only changes when it is confirmed to be charging or not (in the charger_logic() function)
    # Locking actuator status changes when it is confirmed to have a drone on it (in the charger_logic() function)
    # Fire alarm sensor doesn't change unless there is a fire
    def simulate_sensor_data(self): 
            self.voltage = 17
            self.power = 17
            self.solar_power_charging_rate = 960


    def charger_logic(self):
        while True:
            if self.usage_status:
                print("🔌 " + device_name + ": I am currently charging a drone ✅")
            else:
                print("🔌 " + device_name + ": I am NOT currently charging a drone ❌")

            # Try to find a drones that have low battery from our known devices
            try:
                for device in knownDevices:
                    if(device.split("-")[0] == "Drone"):
                        # Send a request to this device
                        battery_level_code = send_interest_packet("battery_level", device)
                        # If the drone battery is low, get the GPS of the drone
                        if battery_level_code in DataReceived:
                            if float(DataReceived[battery_level_code]) < 80:
                                if not self.usage_status:
                                    print("🔌 " + device_name + ": I found a drone with a low battery of " + str(DataReceived[battery_level_code]) + "%")
                                gps_code = send_interest_packet("gps", device)

                                # Store the location of the drone with a low battery using regex
                                if gps_code in DataReceived:
                                    location = re.findall(r'-?\d+\.\d+|-?\d+', DataReceived[gps_code])
                                    location = [float(i) for i in location]

                                    #If the drone has arrived at the location of the charger
                                    if (math.sqrt((int(self.gps[0]) - location[0])**2 + (int(self.gps[1]) - location[1])**2)) <= 1:
                                        # Charger is being used and the locking actuator is closed
                                        self.usage_status = True
                                        self.locking_actuator_status = True

                        # If the charger is being used
                        if self.usage_status:
                            # Get the GPS of a device from our known devices
                            gps_code = send_interest_packet("gps", device)
                            
                            # If the device is at the location of the charger when the charger is being used
                            if (math.sqrt((int(self.gps[0]) - location[0])**2 + (int(self.gps[1]) - location[1])**2)) <= 1:
                                # Get the battery level of the device
                                battery_level_code = send_interest_packet("battery_level", device)

                                # If we get back the battery level from the device and it is fully charged, 
                                # the charger is not being used anymore and the locking actuator is open
                                if battery_level_code in DataReceived:
                                    if float(DataReceived[battery_level_code]) >= 100:
                                        self.usage_status = False
                                        self.locking_actuator_status = False

            except RuntimeError as e: continue
            # Wait one second before trying to find a new drone with a low battery again
            time.sleep(1)


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
                    print("🔌 " + device_name + ": Connected to " + str(discovery_port) + " and my known devices are " + str(knownDevices).replace("u'", "'"))

            # Close socket to allow other devices to connect
            discovery_socket.close()
        except socket.error as e:
            device_socket.sendto(discovery_message+public_key, (discovery_ip[0], discovery_port))
                
        # Wait for 1 seconds before trying to discover more devices
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
            print("🛸 " + device_name + ": No response from " + device + ", performing flooding using my known devices! 🌊")
            for devices in knownDevices:
                device_socket.sendto(encrypt(packet, knownPublicKeys[str(knownDevices[devices])]), knownDevices[devices])
            time.sleep(0.1)
    time.sleep(0.2)
    return requestCode


# Handle an interest request coming from another device
def handle_interests(message, address):
    global responding
    if responding or address != knownDevices["Drone-1"]:
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
                print("🔌 " + device_name + ": Sending requested data from table")
                try:
                    device_socket.sendto(encrypt(message, knownPublicKeys[str(forwardingTable[str(requested_device)+"/"+str(requested_data)])]), forwardingTable[str(requested_device)+"/"+str(requested_data)])
                except Exception:
                    pass
            # If the requested data is not in the forwarding table, perform flooding (contact all known devices)
            else:
                print("🔌 " + device_name + ": Forwarding packet")
                for device in knownDevices:
                    if knownDevices[device] != address: # Make sure to not send the interest back to the sender
                        try:
                            device_socket.sendto(encrypt(message, knownPublicKeys[str(knownDevices[device])]), knownDevices[device])
                        except Exception:
                            continue
        # Once we interact with a drone once, we can mimic network issues from harsh conditions (wind, environmental factors etc) and not respond from now on.
        responding = False
    else:
        print("🔌 " + device_name + ": Blocked message from Drone-1" + str(address))
        


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
        device_socket.sendto(message, interestForwards[interest_code])
        del interestForwards[interest_code]
    # If the data has not been requested, perform flooding
    elif interest_code not in dataForwards:
        dataForwards[interest_code] = requested_data
        for device in knownDevices:
                if knownDevices[device] != address: # Make sure you don't send the interest back to the sender
                    device_socket.sendto(message, knownDevices[device])


# Send requested data to an address
def send_requested_data(message, address):
    interest_code = decrypt(message, private_key).split('/')[1]
    requested_device = decrypt(message, private_key).split('/')[2]
    requested_data = decrypt(message, private_key).split('/')[3]
    # Package the data into a packet
    data_response = "data"+"/"+str(interest_code)+"/"+str(requested_device)+"/"+str(getattr(drone_charger, requested_data))
    device_socket.sendto(encrypt(data_response, knownPublicKeys[str(address)]), address)


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
                except AttributeError as e: continue
            else:
                print("🛸 " + device_name + ": Waiting to discover device before responding back (public key needed)")
        except socket.error: 
            continue


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


def signal_handler(sig, frame):
    subprocess.check_output(['kill', '-9', str(os.getpid())])


def main():
    arguments = parseArguments(argparse.ArgumentParser())
    # Set the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Declare global variables
    global drone_charger
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
    global responding

    # Initialise global variables
    drone_charger = DroneCharger()
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
    public_key, private_key = generate_keys() # Generate a pair of public and private keys specific for this drone charger
    device_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket for drone to communicate via UDP
    device_socket.bind((device_ip, device_port)) # Bind drone to specified unique port
    print("🔌  " + device_name + ": socket connected via UDP.")
    responding = True

    # Declare thread for the sensor data simulation (sensor data changing)
    sensor_data_thread = threading.Thread(target=drone_charger.simulate_sensor_data)
    # Declare thread for the charger logic (if the battery of a known drone hits a threshold it communicates with it)
    charger_logic_thread = threading.Thread(target=drone_charger.charger_logic)
    # Declare thread for discovery (to inform every other node it exists at the start)
    discovery_thread = threading.Thread(target=discovery)
    # Declare thread for receiving messages from other nodes
    receive_messages_thread = threading.Thread(target=receive_messages)

    sensor_data_thread.start()
    charger_logic_thread.start()
    discovery_thread.start()
    receive_messages_thread.start()

    while True:
        # Keep running the main thread until the signal handler kills the process
        time.sleep(1)


if __name__ == "__main__":
    main()