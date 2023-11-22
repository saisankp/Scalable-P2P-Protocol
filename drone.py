# -*- coding: utf-8 -*-

import time
import socket
import threading
import re
import math
import os
import signal
import subprocess
import numpy as np
import argparse
from cryptography import generate_keys, encrypt, decrypt


class Drone:
    # Function below by Prathamesh Sai
    def __init__(self):
        self.destination = (0,0) #The current target destination the drone is trying to go to
        self.nearest_charger = (100,100) # Nearest charger to drone
        self.charging = False # If the drone is charging¸
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


    # Function below by Prathamesh Sai
    def simulate_sensor_data(self):
        while True:
            # Move the drone towards the destination
            self.update_gps()
            print("🛸 " + device_name + ": Current location is " + str(self.gps))
            if not self.charging:
                self.battery_level -= 5 # Battery level goes down over time
                print("🛸 " + device_name + ": Current battery percentage is " + str(self.battery_level) + "%")
            else: 
                self.battery_level += min(10, 100-self.battery_level) # If charging, the battery goes up
                if self.battery_level >= 100:
                    # The drone is fully charged hence we update our variables
                    print("🛸 " + device_name + ": Fully charged now! ⚡🔋")
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
    

    # Function below by Sean Dowling
    def update_gps(self):
        # Move towards destination if not already there (using the pythagorean theorem)
        if math.sqrt((self.gps[0] - self.destination[0])**2 + (self.gps[1] - self.destination[1])**2) > 1:
            print("🛸 " + device_name + ": Current target destination is  " + str(self.destination))
            angle = math.atan2(self.destination[1] - self.gps[1], self.destination[0] - self.gps[0])
            distance = math.sqrt((self.destination[0] - self.gps[0])**2 + (self.destination[1] - self.gps[1])**2)
            # Calculate step sizes based on distance
            step_size = min(10, distance)
            step_x = step_size * math.cos(angle)
            step_y = step_size * math.sin(angle)
            # Update coordinates
            self.gps = (self.gps[0] + step_x, self.gps[1] + step_y)


    # Function below by Prathamesh Sai
    def drone_logic(self):
        while True:
            if self.charging:
                print("🛸 " + device_name + ": Currently charging with a battery percentage of " + str(self.battery_level) + "% 🔋")
                time.sleep(1)
            # Check if the battery is low
            if(self.battery_level <= 35):
                # The battery is low so the drone cannot be used for tasks
                self.busy = True
                self.earthquake = False
                self.hurrcane = False
                self.fire = False
                if self.charging == False:
                    if self.battery_level <= 0:
                        # Drone battery ran out before it could find an available charger
                        print("🛸 " + device_name + ": My battery ran out. I'm dead.")
                        subprocess.check_output(['kill', '-9', str(os.getpid())])
                    print("🛸 " + device_name + ": My battery is dangerously low. Ignoring all tasks to find a charger")
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
                                    print("🛸 " + device_name + ": Found a drone charger to charge at!")
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
                # Check wildfire sensors
                try:
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
                                    # A wildfire has been detected. Mark the drone as busy and ask for the wildfire device's GPS location.
                                    gps_code = send_interest_packet("gps", device)
                                    self.busy = True # Mark drone as busy
                                    print("🛸 " + device_name + ": Informed of a detected wildfire 🔥")
                                    if gps_code in DataReceived:
                                        # Extract numbers from string
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
                                if [(DataReceived[anemometer_code]),(DataReceived[barometer_code]),(DataReceived[hygrometer_code]),(DataReceived[thermometer_code]),(DataReceived[rain_gauge_code]),(DataReceived[lightning_detector_code]),(DataReceived[doppler_radar_code]), (DataReceived[storm_surge_sensor_code])].count("True") >= 4:
                                    # A hurricane has been detected. Mark the drone as busy and ask for the hurricane device's GPS location.
                                    gps_code = send_interest_packet("gps", device)
                                    self.busy = True # mark drone as busy
                                    print("🛸 " + device_name + ": Informed of a detected hurricane 🌀")
                                    if gps_code in DataReceived:
                                        # Extract numbers from string
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
                                if [(DataReceived[seismometer_code]),(DataReceived[accelerometer_code]),(DataReceived[inclinometer_code]),(DataReceived[acounsticsensor_code]),(DataReceived[straingauge_code]),(DataReceived[pwavesensor_code]),(DataReceived[swavesensor_code])].count("True") >= 1:
                                    # An earthquake has been detected. Mark the drone as busy and ask for the earthquake device's GPS location.
                                    gps_code = send_interest_packet("gps", device)
                                    self.busy = True
                                    print("🛸 " + device_name + ": Informed of a detected earthquake 🌋")
                                    # If we get a response from the earthquake device for its GPS location, the drone should go to the disaster location
                                    if gps_code in DataReceived:
                                        # Extract location from string using regex
                                        location = re.findall(r'-?\d+\.\d+|-?\d+', DataReceived[gps_code])
                                        self.destination = ([float(i) for i in location])
                                        self.earthquake = True
                                    else:
                                        print("🛸 " + device_name + ": GPS of earthquake device could not be found")
                except RuntimeError as e: continue

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
            elif not math.sqrt((self.gps[0] - self.destination[0])**2 + (self.gps[1] - self.destination[1])**2) > 1  and self.destination != (0,0):
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
                    print("🛸 " + device_name + ": My job is done. I'm going back to base 🏠")

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
                    print("🛸 " + device_name + ": My job is done. I'm going back to base 🏠")

                elif self.fire:
                    print("🛸 " + device_name + ": Arrived at hurricane location. Using actuators...📟")
                    self.water_release = True
                    print("🛸 " + device_name + ": Water released 🧯")
                    self.payload_release = True
                    print("🛸 " + device_name + ": Payload released 📦")
                    self.flashlight_status = True
                    print("🛸 " + device_name + ": Flashlight is on 🔦")
                    self.speaker_status = True
                    print("🛸 " + device_name + ": Speaker is on 🔊")
                    # Disaster has passed
                    self.fire = False
                    print("🛸 " + device_name + ": My job is done. I'm going back to base 🏠")

            # Wait 1 second before trying to cater for a disaster again
            time.sleep(1)


# Function below by Sean Dowling
# Calculate the Euclidean distance to find the minimum distance to a location (whether it is a drone charger, earthquake device etc)
def get_min_distance(locations, drone_position):
    distances = []
    for point in locations:
        distances.append(math.sqrt((int(drone_position[0]) - int(point[0]))**2 + (int(drone_position[1]) - int(point[1]))**2))
    return locations[np.argmin(distances)]


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
                    print("🛸 " + device_name + ": Connected to " + str(discovery_port) + " and my known devices are " + str(knownDevices).replace("u'", "'"))

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
            print("🛸 " + device_name + ": No response from " + device + ", performing flooding using my known devices! 🌊")
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
            print("🛸 " + device_name + ": Sending requested data from table")
            try:
                device_socket.sendto(encrypt(message, knownPublicKeys[str(forwardingTable[str(requested_device)+"/"+str(requested_data)])]), forwardingTable[str(requested_device)+"/"+str(requested_data)])
            except Exception:
                pass
        # If the requested data is not in the forwarding table, perform flooding (contact all known devices)
        else:
            for device in knownDevices:
                if knownDevices[device] != address: # Make sure to not send the interest back to the sender
                    try:
                        print("🛸 " + device_name + ": Forwarding packet to " + device)
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
    data_response = "data"+"/"+str(interest_code)+"/"+str(requested_device)+"/"+str(getattr(drone, requested_data))
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
                print("🛸 " + device_name + ": Waiting to discover device before responding back (public key needed)")
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
    global drone
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
    drone = Drone()
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
    public_key, private_key = generate_keys() # Generate a pair of public and private keys specific for this drone
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
