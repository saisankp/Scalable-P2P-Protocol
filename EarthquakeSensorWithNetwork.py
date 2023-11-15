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


### Sensor stuff
##  variable to artificially trigger an earthquake
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
            print("earthquake:", bool(self.active))
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
            #print(self.output)
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
            #print(self.output)
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
            #print(self.output)
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
            #print(self.output)
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
            #print(self.output)
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
            #print(self.output)
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
            #print(self.output)
            time.sleep(1)
            
# checks if sensors are detedcting an earthquake
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

            #sensor_activations = [self.seismometer_active, self.accelerometer_active, self.inclinometer_active, self.acounsticsensor_active, self.straingauge_active, self.pwavesensor_active, self.swavesensor_active]
            #self.history.append(sum(sensor_activations))
            
            #if sum(sensor_activations) > 3:
                #print("Threshold breached!")


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

    data_response = "data"+"/"+str(interest_code)+"/"+str(requested_device)+"/"+str(getattr(datamonitor, requested_data))

    device_socket.sendto(data_response.encode(), address)


def receive_messages():
    while True:
        print("awaiting messages")
        try:
            data, sender_address = device_socket.recvfrom(1024)
            #print("Received connection: ", sender_address, data.decode())

            # check message is interset request or data
            if data.decode().split('/')[0] == "interest":
                handle_interests(data.decode(), sender_address)

            elif data.decode().split('/')[0] == "data":
                handle_data(data.decode(), sender_address)

        except ConnectionResetError as e: continue


os.system("kill-port 33505")

device_name = "EarthquakeSensor-1"
device_ip = "localhost"
device_port = 33505

discovery_ip = "localhost" 
discovery_port = 33333

# devices are stored as device: (ip, port)
knownDevices = {}
forwardingTable = {} # device + "/" + data: address
interestForwards = {} #{} # interest code: address
interestRequests = {} # interest codes generated by this device
dataForwards = {} # interest code: address
DataReceived = {} # intereset code: data
requestCodeNum = 0

# bind to device unique port
device_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
device_socket.bind((device_ip, device_port))
print("UDP socket connected")


earthquake = Earthquake()
datamonitor = DataMonitor()
acounsticsensor = AcousticSensor()
inclinometer = Inclinometer()
straingauge = StrainGauge()
accelerometer = Accelerometer()
seismometer = Seismometer()
pwavesensor = PwaveSensor()
swavesensor = SwaveSensor()

# define threads
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

# Start threads
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

# plot outputs
plt.plot(earthquake.history)
plt.plot(datamonitor.history)
#plt.plot(seismometer.history)
#plt.plot(accelerometer.history)
#plt.plot(inclinometer.history)
#plt.plot(straingauge.history)
#plt.plot(acounsticsensor.history)
#plt.plot(pwavesensor.history)
#plt.plot(swavesensor.history)
plt.show
