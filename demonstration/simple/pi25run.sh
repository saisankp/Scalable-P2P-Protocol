# IP Addresses on your Raspberry Pi can be found with
# ip address show | grep "inet "

source env/bin/activate

# Demonstration 1 (simple) - PI #27 has a drone and a hurricane device

python drone.py --device-name Drone-2 --device-ip 10.35.70.25 --device-port 33506 --discovery-ip 0.0.0.0 10.35.70.2 10.35.70.27 --discovery-port 33800
python hurricanedevice.py --device-name HurricaneDevice-1 --device-ip 10.35.70.25 --device-port 33509 --discovery-ip 0.0.0.0 10.35.70.2 10.35.70.27 --discovery-port 33800