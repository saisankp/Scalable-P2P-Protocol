
import time
import socket
import threading
import re
import math
import os
import signal
import sys
import subprocess
import numpy as np
import argparse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

class Drone:
    def __init__(self):
        self.destination = (0,0) #The current target destination the drone is trying to go to
        self.nearest_charger = (100,100) # Nearest available charger
        self.charging = False # If the drone is charging
        self.busy = False # If the drone is busy doing a task
        self.gps = (0, 0) # Latitude, Longitude
        self.battery_level = 100 # Battery percentage
        self.propeller_speed = 0 # Revolutions per minute (RPM)
        self.barometric_pressure = 1013 # Hectopascals (hPa) at sea-level
        self.earthquake = False # If an earthquake occured that we need to help
        self.fire = False # If a fire occured that we need to help
        self.hurricane = False # If a hurricane occured that we need to help
        self.water_release = False # Status of waterload on drone
        self.payload_release = False # Status of payload on drone
        self.speaker_status = False # Status of speaker on drone
        self.flashlight_status = False # Status of flashlight load on drone

    def simulate_sensor_data(self):
        while True:
            # Move the drone towards the destination
            self.update_gps()
            print("🛸 " + device_name + ": current location is " + str(self.gps))
            if not self.charging:
                self.battery_level -= 5 # Battery level goes down over time
                print("🛸 " + device_name + ": current battery percentage is " + str(self.battery_level))
            else: 
                self.battery_level += 10 # If charging, the battery goes up
                print("🛸 " + device_name + ": currently charging with a battery percentage of " + str(self.battery_level) + "% 🔋")
                if self.battery_level >= 100:
                    # The drone is fully charged hence we update our variables
                    print("🛸 " + device_name + ": fully charged now! ⚡")
                    self.charging = False
                    self.busy = False
                    self.destination = (0,0)

            # Increase the propeller speed until it maxes out at 10,000 RPM
            if(self.propeller_speed < 10000):
                self.propeller_speed += 2000

            # As the drone goes up, the barometric pressure decreases until it maxes out at 920 hPa (for its maximum altitude it can go to)
            if(self.barometric_pressure > 920):
                self.barometric_pressure -= 20
            
            # Allow time for the sensor data to update
            time.sleep(2)
    

    def update_gps(self):
        # Move towards destination if not already there (using the pythagorean theorem)
        if math.sqrt((self.gps[0] - self.destination[0])**2 + (self.gps[1] - self.destination[1])**2) > 1:
            print("🛸 " + device_name + ": current target destination is  " + str(self.destination))
            angle = math.atan2(self.destination[1] - self.gps[1], self.destination[0] - self.gps[0])
            distance = math.sqrt((self.destination[0] - self.gps[0])**2 + (self.destination[1] - self.gps[1])**2)
            # Calculate step sizes based on distance
            step_size = min(10, distance)
            step_x = step_size * math.cos(angle)
            step_y = step_size * math.sin(angle)
            # Update coordinates
            self.gps = (self.gps[0] + step_x, self.gps[1] + step_y)


    def drone_logic(self):
        while True:
            # Check if the battery is low
            if(self.battery_level <= 25):
                # The battery is low so the drone cannot be used for tasks
                self.busy = True 
                self.earthquake = False
                self.hurrcane = False
                self.fire = False
                if self.charging == False:
                    # Try to find a charger
                    available_charger_locations = []
                    for device in knownDevices:
                        if(device.split("-")[0] == "Charger"):
                            # Send a request to the charger
                            usage_status_code = send_interest_packet("usage_status", device)
                            usage_voltage_code = send_interest_packet("voltage", device)
                            temperature_code = send_interest_packet("temperature", device)
                            locking_actuator_code = send_interest_packet("locking_actuator_status", device)

                            # If the charger is available, get the GPS of the charger so the drone can go towards it.
                            if usage_status_code in DataReceived and usage_voltage_code in DataReceived and temperature_code in DataReceived and locking_actuator_code in DataReceived:
                                if DataReceived[usage_status_code] == "False" and DataReceived[usage_voltage_code] == "17" and int(DataReceived[temperature_code]) < 40 and DataReceived[locking_actuator_code] == "False":
                                    gps_code = send_interest_packet("gps", device)
                                    # If we receive an answer from the charger which states its GPS location, then we set our destination with it
                                    if gps_code in DataReceived:
                                        # Extract location from string using regex
                                        location = re.findall(r'-?\d+\.\d+|-?\d+', DataReceived[gps_code])
                                        available_charger_locations.append([float(i) for i in location])
                    
                    # If the amount of available chargers is greater than zero
                    if len(available_charger_locations) > 0:
                        # Get the charger that is the least distance away (i.e. the closest)
                        self.destination = get_min_distance(available_charger_locations, self.gps)
                        self.nearest_charger = get_min_distance(available_charger_locations, self.gps)
                    # If the drone is at the charger, update our variables accordingly
                    if not math.sqrt((self.gps[0] - self.nearest_charger[0])**2 + (self.gps[1] - self.nearest_charger[1])**2) > 1 and self.nearest_charger != (0,0):
                        self.charging = True
                     

            # If the drone has enough battery, it should attend to disasters
            if not self.busy:
                # Check earthquake sensors
                for device in knownDevices:
                    if device.split("-")[0] == "WildfireDevice":
                        smoke_particle_sensor_code = send_interest_packet("smoke_particle_sensor_active", device)
                        infrared_sensor_code = send_interest_packet("infrared_sensor_active", device)
                        gas_sensor_code = send_interest_packet("gas_sensor_active", device)
                        wind_sensor_code = send_interest_packet("wind_sensor_active", device)
                        humidity_sensor_code = send_interest_packet("humidity_sensor_active", device)
                        temperature_probe_code = send_interest_packet("temperature_probe_active", device)
                        fire_radiometer_code = send_interest_packet("fire_radiometer_active", device)
                        sensor_codes = [smoke_particle_sensor_code,infrared_sensor_code,gas_sensor_code,wind_sensor_code,humidity_sensor_code,temperature_probe_code,fire_radiometer_code]
                        
                        # Check if at least half of the sensors are sensors are detecting a fire
                        if all(key in DataReceived for key in sensor_codes):
                            if [(DataReceived[smoke_particle_sensor_code]),(DataReceived[infrared_sensor_code]),(DataReceived[gas_sensor_code]),(DataReceived[wind_sensor_code]),(DataReceived[humidity_sensor_code]),(DataReceived[temperature_probe_code]),(DataReceived[fire_radiometer_code])].count("True") >= 6:
                                    # A wildfire has been detected. Mark the drone as busy and ask for the wildfire sensor's GPS location.
                                gps_code = send_interest_packet("gps", device)
                                self.busy = True # Mark drone as busy
                                print("🛸 " + device_name + ": informed of a detected wildfire 🔥")

                                if gps_code in DataReceived:
                                    # extract numbers from string
                                    location = re.findall(r'-?\d+\.\d+|-?\d+', DataReceived[gps_code])
                                    self.destination = ([float(i) for i in location])
                                    self.fire = True
                                else: 
                                    print("🛸 " + device_name + ": GPS of wildfire device could not be found")
                    elif device.split("-")[0] == "HurricaneDevice":
                        anemometer_code = send_interest_packet("anemometer_active", device)
                        barometer_code = send_interest_packet("barometer_active", device)
                        hygrometer_code = send_interest_packet("hygrometer_active", device)
                        thermometer_code = send_interest_packet("thermometer_active", device)
                        rain_gauge_code = send_interest_packet("rain_gauge_active", device)
                        lightning_detector_code = send_interest_packet("lightning_detector_active", device)
                        doppler_radar_code = send_interest_packet("doppler_radar_active", device)
                        storm_surge_sensor_code = send_interest_packet("storm_surge_sensor_active", device)
                        sensor_codes = [anemometer_code,barometer_code,hygrometer_code,thermometer_code,rain_gauge_code,lightning_detector_code,doppler_radar_code,storm_surge_sensor_code]
                        
                        # Check if at least half of the sensors are detecting an hurricane
                        if all(key in DataReceived for key in sensor_codes):
                            if [(DataReceived[anemometer_code]),(DataReceived[barometer_code]),(DataReceived[hygrometer_code]),(DataReceived[thermometer_code]),(DataReceived[rain_gauge_code]),(DataReceived[lightning_detector_code]),(DataReceived[doppler_radar_code]), (DataReceived[storm_surge_sensor_code])].count("True") >= 3:
                                gps_code = send_interest_packet("gps", device)
                                self.busy = True # mark drone as busy
                                print("🛸 " + device_name + ": informed of a detected hurricane 🌀")

                                if gps_code in DataReceived:
                                    # extract numbers from string
                                    location = re.findall(r'-?\d+\.\d+|-?\d+', DataReceived[gps_code])
                                    self.destination = ([float(i) for i in location])
                                    self.hurricane = True
                                else:
                                    print("🛸 " + device_name + ": GPS of hurricane device could not be found")
                    elif(device.split("-")[0] == "EarthquakeDevice"):
                        # The drone has an interest in the values of the sensors in the earthquake device
                        seismometer_code = send_interest_packet("seismometer_active", device)
                        accelerometer_code = send_interest_packet("accelerometer_active", device)
                        inclinometer_code = send_interest_packet("inclinometer_active", device)
                        acounsticsensor_code = send_interest_packet("acounsticsensor_active", device)
                        straingauge_code = send_interest_packet("straingauge_active", device)
                        pwavesensor_code = send_interest_packet("pwavesensor_active", device)
                        swavesensor_code = send_interest_packet("swavesensor_active", device)
                        sensor_codes = [seismometer_code,accelerometer_code,inclinometer_code,acounsticsensor_code,straingauge_code,pwavesensor_code,swavesensor_code]

                        # Check if at least half of the sensors are detecting an earthquake (to stop false positive reactions)
                        if all(key in DataReceived for key in sensor_codes):
                            if sum([bool(DataReceived[seismometer_code]),bool(DataReceived[accelerometer_code]),bool(DataReceived[inclinometer_code]),bool(DataReceived[acounsticsensor_code]),bool(DataReceived[straingauge_code]),bool(DataReceived[pwavesensor_code]),bool(DataReceived[swavesensor_code])]) > 2:
                                # An earthquake has been detected. Mark the drone as busy and ask for the earthquake device's GPS location.
                                gps_code = send_interest_packet("gps", device)
                                self.busy = True
                                print("🛸 " + device_name + ": informed of a detected earthquake 🌋")
                                
                                # If we get a response from the earthquake device for its GPS location, the drone should go to the disaster location
                                if gps_code in DataReceived:
                                    # Extract location from string using regex
                                    location = re.findall(r'-?\d+\.\d+|-?\d+', DataReceived[gps_code])
                                    self.destination = ([float(i) for i in location])
                                    self.earthquake = True
                                else:
                                    print("🛸 " + device_name + ": GPS of earthquake device could not be found")

            # Check if drone has completed current task, send it back to base which is (0,0)
            elif self.payload_release == True or self.flashlight_status == True or self.speaker_status == True or self.water_release == True:
                self.destination = (0,0)
                if not math.sqrt((self.gps[0] - self.destination[0])**2 + (self.gps[1] - self.destination[1])**2) > 1:
                    self.busy = False
                    self.water_release = False
                    self.payload_release = False
                    self.flashlight_status = False
                    self.speaker_status = False

            # Check if the drone is at the earthquake location
            elif not math.sqrt((self.gps[0] - self.destination[0])**2 + (self.gps[1] - self.destination[1])**2) > 1 and self.destination != (0,0):
                if self.earthquake:
                    print("🛸 " + device_name + ": Arrived at earthquake location. Using actuators...📟")
                    self.payload_release = True
                    print("🛸 " + device_name + ": Payload released 📦")
                    self.flashlight_status = True
                    print("🛸 " + device_name + ": Flashlight is on 🔦")
                    self.speaker_status = True
                    print("🛸 " + device_name + ": Speaker is on 🔊")
                    # Disaster has passed
                    self.earthquake = False

                elif self.hurricane:
                    print("🛸 " + device_name + ": Arrived at hurricane location. Using actuators...📟")
                    self.payload_release = True
                    print("🛸 " + device_name + ": Payload released 📦")
                    self.flashlight_status = True
                    print("🛸 " + device_name + ": Flashlight is on 🔦")
                    self.speaker_status = True
                    print("🛸 " + device_name + ": Speaker is on 🔊")
                    # Disaster has passed
                    self.hurrcane = False

                elif self.fire:
                    print("🛸 " + device_name + ": Arrived at hurricane location. Using actuators...📟")
                    self.water_release = True
                    print("🛸 " + device_name + ": water released 🧯")
                    self.payload_release = True
                    print("🛸 " + device_name + ": Payload released 📦")
                    self.flashlight_status = True
                    print("🛸 " + device_name + ": Flashlight is on 🔦")
                    self.speaker_status = True
                    print("🛸 " + device_name + ": Speaker is on 🔊")
                    self.fire = False

            # Wait two seconds before trying to cater for a disaster again
            time.sleep(2)


# Use pythagorean theorem to find the minimum distance to a location (whether it is a drone charger, earthquake device etc)
def get_min_distance(locations, drone_position):
    distances = []
    for point in locations:
        distances.append(math.sqrt((int(drone_position[0]) - int(point[0]))**2 + (int(drone_position[1]) - int(point[1]))**2))
    return locations[np.argmin(distances)]


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
            while time.time() - connection_time < 5:
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
        print("🛸 " + device_name + ": Devices to me are " + str(list(knownDevices.keys())).replace("u'", "'"))
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
            for devices in knownDevices:
                device_socket.sendto(encrypt(packet, knownDevices[devices][1]).encode(), knownDevices[devices][0])
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
            interestForwards[interest_code] = sender_name # add to list of unresolved interests
            # Check if requested data is in forwarding table
            if str(requested_device)+"/"+str(requested_data) in forwardingTable:
                print("🛸 " + device_name + ": Sending requested data from table")
                device_socket.sendto(encrypt(message, knownDevices[sender_name][1]).encode(), forwardingTable[str(requested_device)+"/"+str(requested_data)])
            # If the requested data is not in the forwarding table, perform flooding (contact all known devices)
            else:
                for device in knownDevices:
                    if knownDevices[device] != address: # Make sure to not send the interest back to the sender
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
    data_response = "data"+"/"+str(interest_code)+"/"+str(requested_device)+"/"+str(getattr(drone, requested_data))
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
    global drone
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
    drone = Drone()
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
    print("🛸 " + device_name + ": socket connected via UDP.")

    # Declare thread for the sensor data simulation (sensor data changing)
    sensor_data_thread = threading.Thread(target=drone.simulate_sensor_data)
    # Declare thread for the drone logic (if the battery hits a threshold it tries to find a charger, otherwise it helps other sensors)
    drone_logic_thread = threading.Thread(target=drone.drone_logic)
    # Declare thread for discovery (to inform every other node it exists at the start)
    discovery_thread = threading.Thread(target=discovery)
    # Declare thread for receiving messages from other nodes
    receive_messages_thread = threading.Thread(target=receive_messages)

    sensor_data_thread.start()
    drone_logic_thread.start()
    discovery_thread.start()
    receive_messages_thread.start()

    while True:
        # Keep running the main thread until the signal handler kills the process
        time.sleep(1)


if __name__ == "__main__":
    main()
