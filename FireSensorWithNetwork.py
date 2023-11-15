import time
import random
import threading
import socket
import keyboard
import threading
import os


## Sensor Stuff
class WildfireMonitor:
    def __init__(self):
        # Initialize sensors and set threshold values
        self.smoke_particle_sensor = SmokeParticleSensor(threshold=50)
        self.infrared_sensor = InfraredSensor(threshold=0.8)
        self.gas_sensor = GasSensor(threshold=30)
        self.wind_sensor = WindSensor(threshold_speed=8)
        self.humidity_sensor = HumiditySensor(threshold=40)
        self.temperature_probe = TemperatureProbe(threshold=30)
        self.gps_tracker = GPSTracker()
        self.fire_radiometer = FireRadiometer(threshold=70)

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
            time.sleep(2)


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

    data_response = "data"+"/"+str(interest_code)+"/"+str(requested_device)+"/"+str(getattr(fireMonitor, requested_data))

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


os.system("kill-port 33508")

device_name = "FireSensor-1"
device_ip = "localhost"
device_port = 33508

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
    

fireMonitor = WildfireMonitor()

generate_data_thread = threading.Thread(target=fireMonitor.read_sensors)
discovery_thread = threading.Thread(target=discovery)
receive_messages_thread = threading.Thread(target=receive_messages)

generate_data_thread.start()
discovery_thread.start()
receive_messages_thread.start()
