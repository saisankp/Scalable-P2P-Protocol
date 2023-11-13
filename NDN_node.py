import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message, addr = sock.recvfrom(1024)
            print(f"Received message from {addr}: {message.decode()}")
        except Exception as e:
            print(f"Error receiving message: {str(e)}")

def send_messages(sock, dest_ip, dest_port):
    while True:
        message = input("Enter your message: ")
        sock.sendto(message.encode(), (dest_ip, dest_port))

def main():
    host = '127.0.0.1'
    port = 12345

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    print(f"Listening for incoming messages on {host}:{port}")

    destination_ip = host
    destination_port = port

    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    send_thread = threading.Thread(target=send_messages, args=(sock, destination_ip, destination_port))

    receive_thread.start()
    send_thread.start()

if __name__ == '__main__':
    main()