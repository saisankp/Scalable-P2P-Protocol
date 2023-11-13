import random
import time
import threading
import socket
import keyboard

# Flag to control anemometer data generation
anemometer_enabled = True

# Variables to store sensor data
anemometer_data = 0
barometer_data = 0
hygrometer_data = 0
thermometer_data = 0
rain_gauge_data = 0
lightning_detector_data = 0
doppler_radar_data = 0
storm_surge_sensor_data = 0

# Thresholds for sensors
anemometer_threshold = 80  # Example threshold for high wind speed
barometer_threshold = 1000  # Example threshold for low atmospheric pressure
hygrometer_threshold = 70  # Example threshold for high humidity
thermometer_threshold = 30  # Example threshold for high temperature
rain_gauge_threshold = 10  # Example threshold for heavy rainfall
lightning_detector_threshold = 5  # Example threshold for frequent lightning
doppler_radar_threshold = 100  # Example threshold for intense storm
storm_surge_sensor_threshold = 2  # Example threshold for potential flooding

# FIB (Forwarding Information Base) table
fib_table = []

# Sample node information
node_address = ('localhost', 5000)

# Function to simulate sensor data generation
def generate_sensor_data():
    global anemometer_data, barometer_data, hygrometer_data, thermometer_data
    global rain_gauge_data, lightning_detector_data, doppler_radar_data, storm_surge_sensor_data

    while True:
        
        if anemometer_enabled==True:
            anemometer_data = random.uniform(0, 100)
        barometer_data = random.uniform(950, 1050)
        hygrometer_data = random.uniform(0, 100)
        thermometer_data = random.uniform(-10, 40)
        rain_gauge_data = random.uniform(0, 20)
        lightning_detector_data = random.randint(0, 10)
        doppler_radar_data = random.uniform(0, 200)
        storm_surge_sensor_data = random.uniform(0, 5)

        print("Sensor Data:")
        print(f"Anemometer: {anemometer_data} m/s")
        print(f"Barometer: {barometer_data} hPa")
        print(f"Hygrometer: {hygrometer_data} %")
        print(f"Thermometer: {thermometer_data} °C")
        print(f"Rain Gauge: {rain_gauge_data} mm")
        print(f"Lightning Detector: {lightning_detector_data} strikes")
        print(f"Doppler Radar: {doppler_radar_data} m/s")
        print(f"Storm Surge Sensor: {storm_surge_sensor_data} m\n")

        # Check thresholds and alert if exceeded
        check_thresholds()

        time.sleep(5)

# Function to check thresholds and alert authorities
def check_thresholds():
    # Example: Check anemometer threshold for high wind speed
    if anemometer_data > anemometer_threshold:
        alert_authorities("High wind speed detected!")

    # Example: Check barometer threshold for low atmospheric pressure
    if barometer_data < barometer_threshold:
        alert_authorities("Low atmospheric pressure detected!")

    # Similar checks for other sensors...
    if hygrometer_data > hygrometer_threshold:
        alert_authorities("High humidity detected!")

    if thermometer_data > thermometer_threshold:
        alert_authorities("High temperature detected!")

    if rain_gauge_data > rain_gauge_threshold:
        alert_authorities("Heavy rainfall detected!")

    if lightning_detector_data > lightning_detector_threshold:
        alert_authorities("Frequent lightning detected!")

    if doppler_radar_data > doppler_radar_threshold:
        alert_authorities("Intense storm detected!")

    if storm_surge_sensor_data > storm_surge_sensor_threshold:
        alert_authorities("Potential flooding detected!")

# Function to alert authorities (in this case, send a message to a sample node)
def alert_authorities(message):
    print(f"ALERT: {message}")
    #update_fib_table(message)
    send_alert_message(message)

# Function to send alert message to the sample node
def send_alert_message(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(node_address)
            s.sendall(message.encode())
    except Exception as e:
        print(f"Error sending alert message: {e}")

# Function to update the Forwarding Information Base (FIB) table
def update_fib_table(message):
    global fib_table
    entry = {"timestamp": time.time(), "message": message}
    fib_table.append(entry)
    print("FIB Table Updated:", fib_table)

# Function to simulate sensor failure using keyboard interrupt
def simulate_sensor_failure():
    global anemometer_enabled
    print("Press 's' to stop anemometer data generation.")
    print("Press 'q' to stop the entire program.")
    try:
        while True:
            time.sleep(1)
            if not anemometer_enabled:
                continue

    except KeyboardInterrupt:
        key_pressed = keyboard.read_event(suppress=True).name
        if key_pressed == 's':
            anemometer_enabled = False
            print("Anemometer data generation stopped.")
        elif key_pressed == 'q':
            print("Program terminated by user.")
            # Exit the script or perform cleanup here if needed
            exit()

if __name__ == "__main__":
    # Start the sensor data generation thread
    sensor_thread = threading.Thread(target=generate_sensor_data)
    sensor_thread.start()

    # Start the sensor failure simulation thread
    failure_thread = threading.Thread(target=simulate_sensor_failure)
    failure_thread.start()

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
