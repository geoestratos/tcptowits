import tkinter as tk
import threading
from Functions.utils import load_sensors, generate_wits_frame
from Functions.sensor_manager import SensorManager
from Functions.tcp_server import TCPServer
import datetime
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),  # Guardar en un archivo
                        logging.StreamHandler()  # Mostrar en la consola
                    ])


class HomeApp(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main = self.master
        self.sensor_manager = SensorManager()  # Instancia del SensorManager
        self.tcp_server = TCPServer()  # Iniciar el servidor TCP

        self.create_widgets()
        self.update_sensor_info()

    def create_widgets(self):
        home_label = tk.Label(self, text="Información de Sensores", font=('Helvetica', 16))
        home_label.pack(pady=20)
        self.sensor_info = tk.Text(self, height=15, width=80)
        self.sensor_info.pack(pady=10)

    def update_sensor_info(self):
        # Ejecutar la carga de datos y la actualización en un hilo separado
        threading.Thread(target=self.fetch_sensor_data).start()

    def fetch_sensor_data(self):
        try:
            self.data = load_sensors()  # Cargar los sensores de nuevo
        except Exception as e:
            logging.error(f"Error al cargar sensores: {e}")
            self.main.after(0, self.update_sensor_info_display, [f"Error al cargar sensores: {e}\n"])
            return

        sensor_data_list = []
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for index, sensor in self.data.iterrows():
            host, port = sensor["IP"], sensor["Port"]
            wits_id = sensor["WITSID"]
            try:
                sensor_data = self.sensor_manager.request_data(host, port)
                sensor_data_list.append({
                    "WITSID": wits_id,
                    "value": sensor_data["counter"]
                })
            except Exception as e:
                logging.error(f"Error al solicitar datos del sensor {host}:{port}: {e}")
                sensor_data_list.append({
                    "WITSID": wits_id,
                    "value": 440.666
                })

        trama_wits = generate_wits_frame(sensor_data_list)
        self.tcp_server.send_to_all(trama_wits)
        self.main.after(0, self.update_sensor_info_display, trama_wits)

    def update_sensor_info_display(self, trama_wits):
        self.sensor_info.delete(1.0, tk.END)
        self.sensor_info.insert(tk.END, trama_wits)
        self.after(2000, self.update_sensor_info)  # Actualiza la información cada 2 segundos

    def on_closing(self):
        try:
            self.sensor_manager.close_all()
            self.tcp_server.stop()  # Detener el servidor TCP
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
