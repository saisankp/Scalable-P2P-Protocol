# IP Addresses on your Raspberry Pi can be found with
# ip address show | grep "inet "

source env/bin/activate

# Demonstration 1 (simple) - PI #27 has a drone charger and a wildfire device

python dronecharger.py --device-name Charger-1 --device-ip 10.35.70.27 --device-port 33512 --discovery-ip 0.0.0.0 10.35.70.2 10.35.70.25 --discovery-port 33800
python dronecharger-RoutingDemonstration.py --device-name Charger-1 --device-ip 10.35.70.27 --device-port 33512 --discovery-ip 0.0.0.0 10.35.70.2 10.35.70.25 --discovery-port 33800
python wildfiredevice.py --device-name WildfireDevice-1 --device-ip 10.35.70.27 --device-port 33515 --discovery-ip 0.0.0.0 10.35.70.2 10.35.70.25 --discovery-port 33800