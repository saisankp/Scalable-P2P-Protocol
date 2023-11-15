source env/bin/activate
python dronecharger.py --device-name Charger-1 --device-ip localhost --device-port 33503 --discovery-ip localhost --discovery-port 33333
python drone.py --device-name Drone-1 --device-ip localhost --device-port 33500 --discovery-ip localhost --discovery-port 33333
python earthquakedevice.py --device-name EarthquakeDevice-1 --device-ip localhost --device-port 33505 --discovery-ip localhost --discovery-port 33333
python wildfiredevice.py --device-name WildfireDevice-1 --device-ip localhost --device-port 33508 --discovery-ip localhost --discovery-port 33333
python hurricanedevice.py --device-name HurricaneDevice-1 --device-ip localhost --device-port 33511 --discovery-ip localhost --discovery-port 33333