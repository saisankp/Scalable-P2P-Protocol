import socket

# Sample server node address
node_address = ('localhost', 5000)

# Function to start the sample node server
def start_sample_node():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(node_address)
        server_socket.listen()

        print(f"Sample node listening on {node_address}")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connection established with {client_address}")
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received message: {data.decode()}")

# Start the sample node server
if __name__ == "__main__":
    start_sample_node()
