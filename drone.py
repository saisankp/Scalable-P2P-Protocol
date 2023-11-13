import asyncio
import json

class DroneNode:
    def __init__(self, icn_host, icn_port):
        self.icn_host = icn_host
        self.icn_port = icn_port
        self.gps = (53, -6) # Latitude, Longitude of TCD
        self.battery_level = 100 # Battery percentage
        self.propeller_speed = 0 # RPM
        self.barometric_pressure = 1013 # hPa (of sea-level)
        self.water_release = False
        self.payload_release = False
        self.speaker_status = False
        self.flashlight_status = False


    async def connect_to_icn(self):
        while True:
            try:
                reader, writer = await asyncio.open_connection(self.icn_host, self.icn_port)
                break
            except (ConnectionRefusedError, OSError):
                print("ICN server not available. Retrying...")
                await asyncio.sleep(2)

        async def send_message(message):
            writer.write(message.encode())
            await writer.drain()
            await asyncio.sleep(0.1)
        
        def simulate_sensor_data(): 
            self.gps = (self.gps[0] + 2, self.gps[1] - 1)
            self.battery_level -= 5
            if(self.propeller_speed < 10000):
                self.propeller_speed += 2000
            if(self.barometric_pressure > 920):
                self.barometric_pressure -= 20

        async def send_updates_on_sensor_data():
            sensor_data = {
            "GPS": {"latitude": self.gps[0], "longitude": self.gps[1]},
            "Battery Level": self.battery_level,
            "Propeller Speed": self.propeller_speed,
            "Barometric Pressure": self.barometric_pressure,
            "Water Release Mechanism Status": self.water_release,
            "Payload Release Mechanism Status": self.payload_release,
            "Speaker Status": self.speaker_status,
            "Flashlight Status": self.flashlight_status
            }

            # Convert the dictionary to a JSON string
            json_data = json.dumps(sensor_data)
            await send_message(json_data)


            # await send_message(f"GPS: {self.gps[0]}, {self.gps[1]}")
            # await send_message(f"Battery level: {self.battery_level}")
            # await send_message(f"Propeller speed: {self.propeller_speed}")
            # await send_message(f"Barometric pressure: {self.barometric_pressure}")
            # await send_message(f"Water release mechanism status: {self.water_release}")
            # await send_message(f"Payload release mechanism status: {self.payload_release}")
            # await send_message(f"Speaker status: {self.speaker_status}")
            # await send_message(f"Flashlight status: {self.flashlight_status}")


            


        async def receive_messages():
            while True:
                data = await reader.read(100)
                if not data:
                    break

                message = data.decode()
                print(f"Received message from ICN: {message}")

                if "New node connected" in message:
                    print("New node joined the network!")

        asyncio.create_task(receive_messages())

        # Send a signal to inform the ICN server about the drone
        await send_message("Drone connected")
        await send_updates_on_sensor_data()

        # Simulate some activity (replace this with your actual drone logic)
        while True:
            simulate_sensor_data()
            await asyncio.sleep(1)
            # battery_percentage = self.battery_level
            # await send_message(f"Battery level: {battery_percentage}")
            await send_updates_on_sensor_data()

            if self.battery_level < 90:
                print("Low battery, checking charger availability...")
                await send_message("Charger availability?")


if __name__ == "__main__":
    icn_host = '127.0.0.1'  # Change this to the ICN server's address
    icn_port = 8000  # Change this to the ICN server's port
    drone_node = DroneNode(icn_host, icn_port)
    asyncio.run(drone_node.connect_to_icn())
