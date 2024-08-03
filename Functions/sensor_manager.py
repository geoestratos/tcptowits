import socket
import logging
from time import sleep
import json
# Configuración del logging
logging.basicConfig(level=logging.INFO)
class SensorManager:
    def __init__(self):
        self.connections = {}

    def connect(self, host, port):
        if (host, port) not in self.connections:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(.5)
                sock.connect((host, port))
                self.connections[(host, port)] = sock
                logging.info(f"Conexión establecida con el sensor {host}:{port}")
            except Exception as e:
                logging.error(f"Error al conectar con el sensor {host}:{port}: {e}")
                return None
        return self.connections[(host, port)]

    def request_data(self, host, port):
        sock = self.connect(host, port)
        if sock is None:
            raise ConnectionError(f"Error al conectar con el sensor {host}:{port}")
        try:
            sock.sendall(b"REQUEST DATA")
            response = sock.recv(1024)
            return json.loads(response.decode().strip())  # Suponiendo que el sensor envía JSON
        except socket.timeout:
            logging.error(f"Timeout al intentar conectar con el sensor {host}:{port}")
            raise TimeoutError(f"Timeout al intentar conectar con el sensor {host}:{port}")
        except (socket.error, Exception) as e:
            logging.error(f"Error de socket al conectar con el sensor {host}:{port}: {e}")
            sock.close()
            del self.connections[(host, port)]
            raise ConnectionError(f"Error de socket al conectar con el sensor {host}:{port}: {e}")

    def close_all(self):
        for sock in self.connections.values():
            try:
                sock.close()
            except Exception as e:
                logging.error(f"Error al cerrar la conexión: {e}")
        self.connections.clear()
        logging.info("Todas las conexiones han sido cerradas")
