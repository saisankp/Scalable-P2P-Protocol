import threading
import random
import time
import matplotlib.pyplot as plt
import numpy as np

##  variable to artificially trigger an earthquake
class Earthquake:
    def __init__(self):
        self.active = 0
        self.start = 0
        self.history = []

    def trigger_earthquake(self):
    
        for i in range(2000):
            
                if self.active:
                    if i - self.start > 300:
                        self.active = 0

                else:
                    rand  = random.randrange(1, 800)
                    if rand == 1 and i - self.start > 600:
                        self.start = i
                        self.active = 1

                self.history.append(self.active)
                #print("earthquake:", bool(self.active))
                time.sleep(0.00001)


class Seismometer:
    def __init__(self):
        self.output = 0
        self.history = []
        self.active = 1
        self.triggered = 0
        self.threshold = .5

    def generate_data(self):        
        high = 1
        low = .05
        amplitude = .1

        for i in range(2000):

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
            #print(self.output)
            time.sleep(0.00001)


class Accelerometer:
    def __init__(self):
        self.output = 0
        self.history = []
        self.active = 1
        self.triggered = 0
        self.threshold = .5

    def generate_data(self):
        for i in range(2000):
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
            #print(self.output)
            time.sleep(0.00001)

class Inclinometer:
    def __init__(self):
        self.output = 0
        self.history = []
        self.active = 1
        self.triggered = 0
        self.threshold = .5

    def generate_data(self):
        for i in range(2000):
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
            #print(self.output)
            time.sleep(0.00001)


class StrainGauge:
    def __init__(self):
        self.output = 0
        self.history = []
        self.active = 1
        self.triggered = 0
        self.threshold = .5

    def generate_data(self):
        
        high = .1
        amplitude = 0
        c = 0

        for i in range(2000):

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
            #print(self.output)
            time.sleep(0.00001)


class AcousticSensor:
    def __init__(self):
        self.output = 0
        self.history = []
        self.active = 1
        self.triggered = 0
        self.threshold = .5

    def generate_data(self):
        for i in range(2000):
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
            #print(self.output)
            time.sleep(0.00001)


class PwaveSensor:
    def __init__(self):
        self.output = 0
        self.history = []
        self.active = 1
        self.triggered = 0
        self.threshold = .25

    def generate_data(self):        
        high = .5
        low = .05
        amplitude = .1

        for i in range(2000):

            #if (not earthquake.active):
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
            #print(self.output)
            time.sleep(0.00001)


class SwaveSensor:
    def __init__(self):
        self.output = 0
        self.history = []
        self.active = 1
        self.triggered = 0
        self.threshold = .5

    def generate_data(self):        
        high = 1
        low = .1
        amplitude = .1

        for i in range(2000):

            #if (not earthquake.active):
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
            #print(self.output)
            time.sleep(0.00001)
                
# checks if sensors are detedcting an earthquake
class DataMonitor:
    def __init__(self):
        self.history = []

    def monitor_data(self):
        
        for i in range(2000):
            time.sleep(0.00001)
            seismometer_active = abs(seismometer.output) > seismometer.threshold
            accelerometer_active = abs(accelerometer.output) > accelerometer.threshold
            inclinometer_active = abs(inclinometer.output) > acounsticsensor.threshold
            acounsticsensor_active = acounsticsensor.output > acounsticsensor.threshold
            straingauge_active = straingauge.output > straingauge.threshold
            pwavesensor_active = abs(pwavesensor.output) > pwavesensor.threshold
            swavesensor_active = abs(swavesensor.output) > swavesensor.threshold

            sensor_activations = [seismometer_active, accelerometer_active, inclinometer_active, acounsticsensor_active, straingauge_active, pwavesensor_active, swavesensor_active]
            self.history.append(sum(sensor_activations))

            if sum(sensor_activations) > 3:
                print("Threshold breached!", i)


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

# wait for thread to finish
trigger_earthquake_thread.join()
seismometer_thread.join()
accelerometer_thread.join()
inclinometer_thread.join()
acounsticsensor_thread.join()
straingauge_thread.join()
pwavesensor_thread.join()
swavesensor_thread.join()
data_monitoring_thread.join()

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