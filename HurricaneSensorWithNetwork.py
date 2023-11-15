import random
import time
import threading
import socket
import keyboard
import threading
import os

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

            time.sleep(2)

    def check_thresholds(self):
        if self.anemometer_data > self.anemometer_threshold:
            self.alert_authorities("High wind speed detected!")

        if self.barometer_data < self.barometer_threshold:
            self.alert_authorities("Low atmospheric pressure detected!")

        if self.hygrometer_data > self.hygrometer_threshold:
            self.alert_authorities("High humidity detected!")

        if self.thermometer_data > self.thermometer_threshold:
            self.alert_authorities("High temperature detected!")

        if self.rain_gauge_data > self.rain_gauge_threshold:
            self.alert_authorities("Heavy rainfall detected!")

        if self.lightning_detector_data > self.lightning_detector_threshold:
            self.alert_authorities("Frequent lightning detected!")

        if self.doppler_radar_data > self.doppler_radar_threshold:
            self.alert_authorities("Intense storm detected!")

        if self.storm_surge_sensor_data > self.storm_surge_sensor_threshold:
            self.alert_authorities("Potential flooding detected!")

    def keyboard_interrupt(self):
        print("Press 's' to stop anemometer data generation.")
        print("Press 'q' to stop the entire program.")
        while self.running:
            key_event = keyboard.read_event(suppress=True)
            key_pressed = key_event.name
            if key_pressed == 's':
                self.anemometer_enabled = False
                self.anemometer_data = 0
                print("Anemometer data generation stopped.")
            elif key_pressed == 'q':
                self.stop_monitoring()

############################################################

### Network stuff

def discovery():
    while True:
        discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discovery_message = device_name
        try:
            # Check if port is available
            discovery_socket.bind((discovery_ip, discovery_port))
            discovery_socket.settimeout(1)
            connection_time = time.time()

            # Hold the connection for 2 seconds to listen for incoming discovery messages
            while time.time() - connection_time < 2:
                try:
                    data, sender_address = discovery_socket.recvfrom(1024)
                    knownDevices[data.decode()] = sender_address
                except socket.timeout:
                    continue

            # Close socket to allow other devices to connect
            discovery_socket.close()
        except OSError as e:
            # Send discovery message to the receiver
            device_socket.sendto(discovery_message.encode(), (discovery_ip, discovery_port))

        time.sleep(1)


# send an interest packet for a piece of data on a different device
def send_interest_packet(data, device):
    global requestCodeNum
    requestCodeNum = requestCodeNum + 1
    requestCode = str(device_name)+str(requestCodeNum)

    packet = "interest"+"/"+requestCode+"/"+str(device)+"/"+str(data)
    interestRequests[requestCode] = [str(device), str(data)]

    # if no specific devices are mentioned in the call
    if device == "none":
        # check if data is in the forwarding table
        if str(device)+"/"+str(data) in forwardingTable:
                device_socket.sendto(packet.encode(), forwardingTable[str(device)+"/"+str(data)])
                #awaitedAcks[requestCode] = [packet, time.time()]

        # if not perform flooding
        else:
            for devices in knownDevices:
                device_socket.sendto(packet.encode(), knownDevices[devices])

    else:
        device_socket.sendto(packet.encode(), knownDevices[device])

    return requestCode


def handle_interests(message, address):

    interest_code = message.split('/')[1]
    requested_device = message.split('/')[2]
    requested_data = message.split('/')[3]

    # if this is the requested device, send the info
    if requested_device == device_name:
        send_requested_data(message, address)

    # else forward the packet if it hasnt been already
    elif interest_code not in interestForwards:

        interestForwards[interest_code] = address # add to list of unresolved interests

        # check if requested data is in forwarding table
        if str(requested_device)+"/"+str(requested_data) in forwardingTable:
            print("sending from table")
            device_socket.sendto(message.encode(), forwardingTable[str(requested_device)+"/"+str(requested_data)])
            #awaitedAcks[interest_code] = [message, time.time()]

        # if not perform flooding
        else:
            for device in knownDevices:
                if knownDevices[device] != address: # dont send the interest back to the sender
                    device_socket.sendto(message.encode(), knownDevices[device])


def handle_data(message, address):

    interest_code = message.split('/')[1]
    requested_device = message.split('/')[2]
    requested_data = message.split('/')[3]

    # add sender to forwarding table
    forwardingTable[str(requested_device)+"/"+str(requested_data)] = address

    # if interest request was made by this device
    if interest_code in interestRequests:
        #print("data received:", message)
        DataReceived[interest_code] = requested_data
        del interestRequests[interest_code]

    # if not forward to the correct device
    elif interest_code in interestForwards:
        device_socket.sendto(message.encode(), interestForwards[interest_code])
        #awaitedAcks[interest_code] = [message, time.time()]
        del interestForwards[interest_code]

    # if this data has not been requested perform flooding
    elif interest_code not in dataForwards:
        dataForwards[interest_code] = requested_data
        for device in knownDevices:
                if knownDevices[device] != address: # dont send the interest back to the sender
                    device_socket.sendto(message.encode(), knownDevices[device])


def send_requested_data(message, address):
    interest_code = message.split('/')[1]
    requested_device = message.split('/')[2]
    requested_data = message.split('/')[3]

    data_response = "data"+"/"+str(interest_code)+"/"+str(requested_device)+"/"+str(getattr(hurricaneDevice, requested_data))

    device_socket.sendto(data_response.encode(), address)


def receive_messages():
    while True:
        try:
            data, sender_address = device_socket.recvfrom(1024)
            #print("Received connection: ", sender_address, data.decode())

            # check message is interset request or data
            if data.decode().split('/')[0] == "interest":
                handle_interests(data.decode(), sender_address)

            elif data.decode().split('/')[0] == "data":
                handle_data(data.decode(), sender_address)

        except ConnectionResetError as e: continue


os.system("kill-port 33506")

device_name = "HurricaneSensor-1"
device_ip = "localhost"
device_port = 33506

discovery_ip = "localhost" 
discovery_port = 33333

# devices are stored as device: (ip, port)
knownDevices = {}
forwardingTable = {} # device + "/" + data: address
interestForwards = {} #{} # interest code: address
interestRequests = {} # interest codes generated by this device
dataForwards = {} # interest code: address
DataReceived = {} # interest code: data
requestCodeNum = 0

# bind to device unique port
device_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
device_socket.bind((device_ip, device_port))
print("UDP socket connected")


hurricaneDevice = HurricaneDevice()

generate_data_thread = threading.Thread(target=hurricaneDevice.generate_sensor_data)
discovery_thread = threading.Thread(target=discovery)
receive_messages_thread = threading.Thread(target=receive_messages)

generate_data_thread.start()
discovery_thread.start()
receive_messages_thread.start()
