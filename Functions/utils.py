import pandas as pd
import json
import socket
import datetime
def load_sensors(filename="sensors.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return pd.DataFrame(data)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar datos desde {filename}: {e}")
        return pd.DataFrame({'IP': [], 'Port': [], 'WITSID': []})

def save_sensors(data, filename="sensors.json"):
    try:
        data.to_dict('records')  # Convertir DataFrame a lista de diccionarios
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print("Datos guardados correctamente en JSON.")
    except Exception as e:
        print(f"Error al guardar datos en JSON: {e}")

def add_sensor(ip, port, filename="sensors.json"):
    sensors = load_sensors(filename)
    sensors.append({"ip": ip, "port": port})
    save_sensors(sensors, filename)


def request_sensor_data(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(.1)
            sock.connect((host, port))
            sock.sendall(b"REQUEST DATA")
            response = sock.recv(1024)
            return response.decode()
    except socket.timeout:
        return f"Timeout al intentar conectar con el sensor {host}"
    except Exception as e:
        return f"Error al conectar o recibir datos del sensor {host}: {str(e)}"