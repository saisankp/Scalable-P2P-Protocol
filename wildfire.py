import time
import random

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

    def read_sensors(self):
        smoke_level = self.smoke_particle_sensor.detect_smoke()
        infrared_data = self.infrared_sensor.measure_infrared()
        gas_level = self.gas_sensor.detect_gas()
        wind_direction, wind_speed = self.wind_sensor.measure_wind()
        humidity_level = self.humidity_sensor.measure_humidity()
        temperature = self.temperature_probe.measure_temperature()
        gps_location = self.gps_tracker.get_location()
        fire_intensity = self.fire_radiometer.measure_fire_intensity()

        # Process sensor data and check for alerts
        self.process_data(smoke_level, infrared_data, gas_level, wind_direction, wind_speed,
                          humidity_level, temperature, gps_location, fire_intensity)

    def process_data(self, smoke_level, infrared_data, gas_level, wind_direction, wind_speed,
                     humidity_level, temperature, gps_location, fire_intensity):
        # Check for alerts based on threshold values
        if smoke_level > self.smoke_particle_sensor.threshold:
            self.trigger_alert("Smoke Alert!")
        if infrared_data > self.infrared_sensor.threshold:
            self.trigger_alert("Infrared Alert!")
        if gas_level > self.gas_sensor.threshold:
            self.trigger_alert("Gas Alert!")
        if wind_speed > self.wind_sensor.threshold_speed:
            self.trigger_alert("High Wind Alert!")
        if humidity_level < self.humidity_sensor.threshold:
            self.trigger_alert("Low Humidity Alert!")
        if temperature > self.temperature_probe.threshold:
            self.trigger_alert("High Temperature Alert!")
        if fire_intensity > self.fire_radiometer.threshold:
            self.trigger_alert("High Fire Intensity Alert!")

        # Display monitoring data
        self.display_data(smoke_level, infrared_data, gas_level, wind_direction, wind_speed,
                          humidity_level, temperature, gps_location, fire_intensity)

    def display_data(self, smoke_level, infrared_data, gas_level, wind_direction, wind_speed,
                     humidity_level, temperature, gps_location, fire_intensity):
        # Display monitoring data (you can customize this based on your needs)
        print("Monitoring Data:")
        print(f"Smoke Level: {smoke_level}")
        print(f"Infrared Data: {infrared_data}")
        print(f"Gas Level: {gas_level}")
        print(f"Wind Direction: {wind_direction}, Wind Speed: {wind_speed}")
        print(f"Humidity Level: {humidity_level}")
        print(f"Temperature: {temperature}")
        print(f"GPS Location: {gps_location}")
        print(f"Fire Intensity: {fire_intensity}")
        print("\n")

    def trigger_alert(self, message):
        # Implement alert mechanism (send email, SMS, etc.)
        print(f"ALERT: {message}")

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

if __name__ == "__main__":
    wildfire_monitor = WildfireMonitor()

    while True:
        wildfire_monitor.read_sensors()
        time.sleep(2)  # Time interval
