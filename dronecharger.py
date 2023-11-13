import asyncio
import json

class DroneChargerNode:
    def __init__(self, icn_host, icn_port):
        self.icn_host = icn_host
        self.icn_port = icn_port
        self.gps = (70, -2) # Latitude, Longitude near TCD
        self.voltage = 0 # Volts
        self.temperature = 10 # Degrees celcius
        self.solar_power_charging_rate = 0 # Wh/m 
        self.usage_status = False
        self.locking_actuator_status = False
        self.fire_alarm_sensor = False
        self.rfid_authenticator_output = None

    async def connect_to_icn(self):
        while True:
            try:
                reader, writer = await asyncio.open_connection(self.icn_host, self.icn_port)
                break
            except (ConnectionRefusedError, OSError):
                print("ICN server not available. Retrying...")
                await asyncio.sleep(2)
        
        def simulate_sensor_data(): 
            #GPS does not change unless it is being transported
            self.voltage = 17
            #Temperature does not change unless there is a fire/stress on power
            self.solar_power_charging_rate = 960
            #Usage status only changes when it is confirmed to be charging
            #Locking actuator status changes when it is confirmed to have a drone on it
            #Fire alarm sensor doesn't change unless there is a fire
            #RFID Authenticator needs to be implemented for SECURITY/ENCRYPTION later on (after networks stuff)
        
        async def send_updates_on_sensor_data():
            sensor_data = {
                "GPS": {"latitude": self.gps[0], "longitude": self.gps[1]},
                "Voltage": self.voltage,
                "Temperature": self.temperature,
                "Solar Power Charging Rate": self.solar_power_charging_rate,
                "Usage Status": self.usage_status,
                "Locking Actuator Status": self.locking_actuator_status,
                "Fire Alarm Sensor": self.fire_alarm_sensor,
                "RFID Authenticator Output": self.rfid_authenticator_output
            }

            # Convert the dictionary to a JSON string
            json_data = json.dumps(sensor_data)
            await send_message(json_data)

        async def send_message(message):
            writer.write(message.encode())
            await writer.drain()
            await asyncio.sleep(0.1)

        async def receive_messages():
            while True:
                data = await reader.read(1000)
                if not data:
                    break

                message = data.decode()
                try:
                    message = json.loads(message)
                    if(message["Battery Level"] < 20):
                        print("I'm a charger, and the drone wants me. ")  
                        print("Drone battery low, checking charger availability...")
                        await send_updates_on_sensor_data()
                except json.JSONDecodeError as e:
                    if "New node connected" in message:
                        print("New node joined the network!")
                    elif "Node disconnected" in message:
                        print("Node disconnected from the network.")
                    elif "Charger availability?" in message:
                        print("I'm a charger, and the drone wants me.")
                        print("Drone battery low, checking charger availability...")
                        await send_updates_on_sensor_data()
                    else:
                        print(f"Received message from ICN: {message}")

        asyncio.create_task(receive_messages())

        # Send a signal to inform the ICN server about the charger
        await send_message("Charger connected")
        simulate_sensor_data()

        # Simulate charger availability (replace this with your actual charger logic)
        while True:
            await asyncio.sleep(20)
            print("Charger available")
    
if __name__ == "__main__":
    icn_host = '127.0.0.1'  # Change this to the ICN server's address
    icn_port = 8000  # Change this to the ICN server's port
    charger_node = DroneChargerNode(icn_host, icn_port)
    asyncio.run(charger_node.connect_to_icn())
