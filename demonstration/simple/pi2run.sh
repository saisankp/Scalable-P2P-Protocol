# IP Addresses on your Raspberry Pi can be found with
# ip address show | grep "inet "

source env/bin/activate

# Demonstration 1 (simple) - PI #2 has a drone and an earthquake device

python drone.py --device-name Drone-1 --device-ip 10.35.70.2 --device-port 33500 --discovery-ip 0.0.0.0 10.35.70.27 10.35.70.25 --discovery-port 33800
python earthquakedevice.py --device-name EarthquakeDevice-1 --device-ip 10.35.70.2 --device-port 33503 --discovery-ip 0.0.0.0 10.35.70.27 10.35.70.25 --discovery-port 33800