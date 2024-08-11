import socket
import threading
import logging

class TCPServer:
    def __init__(self, host='0.0.0.0', port=65432):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.connections = []
        self.is_running = True
        self.thread = threading.Thread(target=self.accept_connections)
        self.thread.start()
        logging.info(f"Servidor TCP iniciado en {self.host}:{self.port}")

    def accept_connections(self):
        while self.is_running:
            client_socket, client_address = self.server_socket.accept()
            logging.info(f"Conexión aceptada de {client_address}")
            self.connections.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while self.is_running:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Manejar los datos recibidos aquí si es necesario
            except socket.error as e:
                logging.error(f"Error en la conexión del cliente: {e}")
                break
        client_socket.close()
        self.connections.remove(client_socket)

    def send_to_all(self, message):
        for client_socket in self.connections:
            try:
                client_socket.sendall(message.encode())
            except socket.error as e:
                logging.error(f"Error al enviar datos a {client_socket.getpeername()}: {e}")
                client_socket.close()
                self.connections.remove(client_socket)

    def stop(self):
        self.is_running = False
        self.server_socket.close()
        for client_socket in self.connections:
            client_socket.close()
        self.connections = []
        logging.info("Servidor TCP detenido")