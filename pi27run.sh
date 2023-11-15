# IP Addresses on your Raspberry Pi can be found with
# ip address show | grep "inet "

# TODO: Decide network configuration for demo

source env/bin/activate

# LOCALHOST NETWORK 
python dronecharger.py --device-name Charger-1 --device-ip localhost --device-port 33503 --discovery-ip localhost --discovery-port 33333
python drone.py --device-name Drone-1 --device-ip localhost --device-port 33500 --discovery-ip localhost --discovery-port 33333

# 10.35.70.2 NETWORK
python drone.py --device-name Drone-2 --device-ip 10.35.70.2 --device-port 33500 --discovery-ip localhost --discovery-port 33333
python drone.py --device-name Charger-1 --device-ip 10.35.70.2 --device-port 33500 --discovery-ip 10.35.70.27 --discovery-port 33333