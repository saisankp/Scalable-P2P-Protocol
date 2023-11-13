import random
import time
import threading
import socket
import keyboard
from datetime import datetime

class HurricaneDevice:
    def __init__(self):
        # Sensor data and thresholds
        self.anemometer_enabled = True
        self.anemometer_data = 0
        self.barometer_data = 0
        self.hygrometer_data = 0
        self.thermometer_data = 0
        self.rain_gauge_data = 0
        self.lightning_detector_data = 0
        self.doppler_radar_data = 0
        self.storm_surge_sensor_data = 0

        self.anemometer_threshold = 80
        self.barometer_threshold = 1000
        self.hygrometer_threshold = 70
        self.thermometer_threshold = 30
        self.rain_gauge_threshold = 10
        self.lightning_detector_threshold = 5
        self.doppler_radar_threshold = 100
        self.storm_surge_sensor_threshold = 2

        # FIB (Forwarding Information Base) table
        self.fib_table = []

        # Sample server node information
        self.node_address = ('localhost', 5000)

        # Socket for communication
        self.client_socket = None

        # Start the keyboard input handling thread
        self.keyboard_thread = threading.Thread(target=self.keyboard_interrupt)

        # Flag to control the main loop
        self.running = False

    def start_monitoring(self):
        self.running = True
        # Start threads
        self.keyboard_thread.start()
        self.generate_sensor_data()

    def stop_monitoring(self):
        self.running = False
        # Close the socket before exiting
        if self.client_socket:
            self.client_socket.close()
        print("Exiting...")

    def generate_sensor_data(self):
        while self.running:
            if self.anemometer_enabled:
                self.anemometer_data = random.uniform(0, 100)
            self.barometer_data = random.uniform(950, 1050)
            self.hygrometer_data = random.uniform(0, 100)
            self.thermometer_data = random.uniform(-10, 40)
            self.rain_gauge_data = random.uniform(0, 20)
            self.lightning_detector_data = random.randint(0, 10)
            self.doppler_radar_data = random.uniform(0, 200)
            self.storm_surge_sensor_data = random.uniform(0, 5)

            # Get the current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print("Sensor Data at Timestamp:", timestamp)
            print(f"Anemometer: {self.anemometer_data} m/s")
            print(f"Barometer: {self.barometer_data} hPa")
            print(f"Hygrometer: {self.hygrometer_data} %")
            print(f"Thermometer: {self.thermometer_data} °C")
            print(f"Rain Gauge: {self.rain_gauge_data} mm")
            print(f"Lightning Detector: {self.lightning_detector_data} strikes")
            print(f"Doppler Radar: {self.doppler_radar_data} m/s")
            print(f"Storm Surge Sensor: {self.storm_surge_sensor_data} m\n")

            # Check thresholds and alert if exceeded
            self.check_thresholds()

            time.sleep(5)

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

    def alert_authorities(self, message):
        print(f"ALERT: {message}")
        self.send_alert_message(message)

    def send_alert_message(self, message):
        try:
            # Check if the socket is not connected
            if self.client_socket is None or self.client_socket.fileno() == -1:
                # Establish a new connection
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect(self.node_address)

            # Send the message
            self.client_socket.sendall(message.encode())
        except Exception as e:
            print(f"Error sending alert message: {e}")
            # Close the socket on error
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None

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

if __name__ == "__main__":
    device1 = HurricaneDevice()
    device1.start_monitoring()
