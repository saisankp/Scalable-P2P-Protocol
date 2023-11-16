# This will be done by Prathamesh (using pi #2) to show how the drones interact with each other device

# First: drone and earthquake device
python drone.py --device-name Drone-1 --device-ip 10.35.70.2 --device-port 33500 --discovery-ip 0.0.0.0 10.35.70.27 10.35.70.25 --discovery-port 33800
python earthquakedevice.py --device-name EarthquakeDevice-1 --device-ip 10.35.70.2 --device-port 33503 --discovery-ip 0.0.0.0 10.35.70.27 10.35.70.25 --discovery-port 33800

# Second: drone and wildfire device
python drone.py --device-name Drone-1 --device-ip 10.35.70.2 --device-port 33500 --discovery-ip 0.0.0.0 10.35.70.27 10.35.70.25 --discovery-port 33800
python wildfiredevice.py --device-name WildfireDevice-1 --device-ip 10.35.70.2 --device-port 33503 --discovery-ip 0.0.0.0 10.35.70.27 10.35.70.25 --discovery-port 33800

# Third: drone and hurricane device
python drone.py --device-name Drone-1 --device-ip 10.35.70.2 --device-port 33500 --discovery-ip 0.0.0.0 10.35.70.27 10.35.70.25 --discovery-port 33800
python hurricanedevice.py --device-name HurricaneDevice-1 --device-ip 10.35.70.2 --device-port 33503 --discovery-ip 0.0.0.0 10.35.70.2 10.35.70.27 --discovery-port 33800

# Change battery decreasing rate to 10 now
# Fourth: drone and drone charger
python drone.py --device-name Drone-1 --device-ip 10.35.70.2 --device-port 33500 --discovery-ip 0.0.0.0 10.35.70.27 10.35.70.25 --discovery-port 33800
python dronecharger.py --device-name Charger-1 --device-ip 10.35.70.2 --device-port 33503 --discovery-ip 0.0.0.0 10.35.70.27 10.35.70.25 --discovery-port 33800