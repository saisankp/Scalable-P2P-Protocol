# IP Addresses on your Raspberry Pi can be found with
# ip address show | grep "inet "

source env/bin/activate

# Demonstration 1 (simple) - PI #27 has a drone, drone charger, earthquake device, hurricane device and wildfire device (5 devices which 8 sensors/actuators each)

python drone.py --device-name Drone-1 --device-ip 10.35.70.27 --device-port 33500 --discovery-ip 0.0.0.0 10.35.70.2 10.35.70.25 --discovery-port 33800
python dronecharger.py --device-name Charger-1 --device-ip 10.35.70.27 --device-port 33503 --discovery-ip 0.0.0.0 10.35.70.2 10.35.70.25 --discovery-port 33800
python earthquakedevice.py --device-name EarthquakeDevice-1 --device-ip 10.35.70.27 --device-port 33503 --discovery-ip 0.0.0.0 10.35.70.2 10.35.70.25 --discovery-port 33800
python hurricanedevice.py --device-name EarthquakeDevice-1  --device-ip 10.35.70.27 --device-port 33503 --discovery-ip 0.0.0.0 10.35.70.2 10.35.70.25 --discovery-port 33800
python wildfiredevice.py --device-name WildfireDevice-1 --device-ip 10.35.70.27 --device-port 33503 --discovery-ip 0.0.0.0 10.35.70.2 10.35.70.25 --discovery-port 33800
