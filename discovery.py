import socket
import threading
import time

device_name = "EarthquakeSensor123"
device_ip = "localhost"
device_port = 33500

discovery_ip = "localhost" 
discovery_port = 33333

# devices are stored as device: (ip, port)
knownDevices = {}

# bind to device unique port
device_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
device_socket.bind((device_ip, device_port))
print("UDP socket connected")

def discovery():
    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_message = device_name
    
    # check if port is available
    try:
        discovery_socket.bind((discovery_ip, discovery_port))
        discovery_socket.settimeout(1)
        connection_time = time.time()

        # hold the connection for 2 seconds to listen for incoming discovery messages
        while time.time()-connection_time < 5:########
            print("awaiting discovery messages")

            try: 
                data, sender_address = discovery_socket.recvfrom(1024)
                print("Received connection: ", sender_address, data.decode())
                knownDevices[data.decode()] = sender_address

            except socket.timeout:
                print()

        # close socket to allow other devices to connect
        discovery_socket.close()
        print("closing discovery socket")

    except OSError as e:
        print("discovery socket in use")

        # Send discovery message to the receiver
        device_socket.sendto(discovery_message.encode(), (discovery_ip, discovery_port))

    time.sleep(3)


discovery_thread = threading.Thread(target=discovery)
discovery_thread.start()
discovery_thread.join()
print(knownDevices)
