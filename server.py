import socket
import threading

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockets = []
        self.shutdown = False

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        # Start the server thread to accept incoming connections.
        server_thread = threading.Thread(target=self.accept_connections)
        server_thread.start()

        # Start the message handling thread.
        message_thread = threading.Thread(target=self.handle_messages)
        message_thread.start()

        print(f"Peer listening on {self.host}:{self.port}")

    def accept_connections(self):
        while not self.shutdown:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection established with {client_address}")
            self.client_sockets.append(client_socket)

    def handle_messages(self):
        while not self.shutdown:
            for client_socket in self.client_sockets:
                try:
                    data = client_socket.recv(1024)
                    if data:
                        message = data.decode('utf-8')
                        print(f"Received message: {message}")
                except Exception as e:
                    print(f"Error while receiving message: {e}")
                    self.client_sockets.remove(client_socket)

    def send_message(self, host, port, message):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            client_socket.sendall(message.encode('utf-8'))
            client_socket.close()
        except Exception as e:
            print(f"Error while sending message to {host}:{port}: {e}")

    def stop(self):
        self.shutdown = True
        self.server_socket.close()

if __name__ == "__main__":
    my_peer = Peer("localhost", 9000)
    my_peer.start()

    while True:
        try:
            dest_host = input("Enter destination host: ")
            dest_port = int(input("Enter destination port: "))
            message = input("Enter your message: ")

            if dest_host == "exit":
                break

            my_peer.send_message(dest_host, dest_port, message)
        except KeyboardInterrupt:
            break

    my_peer.stop()
