import socket
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO)

class SensorManager:
    def __init__(self):
        self.connections = {}

    def connect(self, host, port):
        if (host, port) not in self.connections:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
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
            return f"Error al conectar con el sensor {host}:{port}"
        try:
            sock.sendall(b"REQUEST DATA")
            response = sock.recv(1024)
            return response.decode()
        except socket.timeout:
            logging.error(f"Timeout al intentar conectar con el sensor {host}:{port}")
            return f"Timeout al intentar conectar con el sensor {host}:{port}"
        except socket.error as e:
            logging.error(f"Error de socket al conectar con el sensor {host}:{port}: {e}")
            return f"Error de socket al conectar con el sensor {host}:{port}: {e}"
        except Exception as e:
            logging.error(f"Error inesperado al conectar con el sensor {host}:{port}: {e}")
            return f"Error inesperado al conectar con el sensor {host}:{port}: {e}"

    def close_all(self):
        for sock in self.connections.values():
            try:
                sock.close()
            except Exception as e:
                logging.error(f"Error al cerrar la conexión: {e}")
        self.connections.clear()
        logging.info("Todas las conexiones han sido cerradas")
