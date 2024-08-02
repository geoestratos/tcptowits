import tkinter as tk
from tkinter import ttk
import threading
from Functions.utils import load_sensors
from Functions.sensor_manager import SensorManager
import datetime
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO)

class HomeApp(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main = self.master
        self.sensor_manager = SensorManager()  # Instancia del SensorManager

        self.create_widgets()
        self.update_sensor_info()

    def create_widgets(self):
        home_label = tk.Label(self, text="Información de Sensores", font=('Helvetica', 16))
        home_label.pack(pady=20)
        self.sensor_info = tk.Text(self, height=15, width=80)
        self.sensor_info.pack(pady=10)

    def update_sensor_info(self):
        try:
            self.data = load_sensors()  # Cargar los sensores de nuevo
            self.sensors = [(row['IP'], row['Port']) for index, row in self.data.iterrows()]
        except Exception as e:
            logging.error(f"Error al cargar sensores: {e}")
            self.sensor_info.insert(tk.END, f"Error al cargar sensores: {e}\n")
            return

        self.sensor_info.delete(1.0, tk.END)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.sensor_info.insert(tk.END, f"Timestamp: {timestamp}\n")

        for host, port in self.sensors:
            try:
                sensor_data = self.sensor_manager.request_data(host, port)
                if "Error" in sensor_data or "Timeout" in sensor_data:
                    self.sensor_info.insert(tk.END, f"{sensor_data}\n")
                else:
                    self.sensor_info.insert(tk.END, f"Sensor {host}:{port} data: {sensor_data}\n")
            except Exception as e:
                logging.error(f"Error al solicitar datos del sensor {host}:{port}: {e}")


        self.after(1000, self.update_sensor_info)  # Actualiza la información cada 2 segundos

    def on_closing(self):
        try:
            self.sensor_manager.close_all()
        except Exception as e:
            logging.error(f"Error al cerrar las conexiones: {e}")
        self.main.destroy()

if __name__ == '__main__':
    try:
        root = tk.Tk()
        app = HomeApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.pack(fill='both', expand=True)
        root.mainloop()
    except Exception as e:
        logging.error(f"Error al iniciar la aplicación: {e}")
