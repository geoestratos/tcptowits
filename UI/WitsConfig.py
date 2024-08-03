import tkinter as tk
from tkinter import ttk

class WitsConfig(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main = self.master
        self.main.title("Configuración WITS")

        self.create_widgets()
        self.pack()

    def create_widgets(self):
        # Etiquetas y entradas para el puerto
        tk.Label(self, text="Puerto:").grid(row=0, column=0, padx=10, pady=10)
        self.port_entry = tk.Entry(self)
        self.port_entry.grid(row=0, column=1, padx=10, pady=10)

        # Etiquetas y entradas para el nombre del pozo
        tk.Label(self, text="Nombre del pozo:").grid(row=1, column=0, padx=10, pady=10)
        self.well_name_entry = tk.Entry(self)
        self.well_name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Etiquetas y entradas para el tiempo de envío
        tk.Label(self, text="Tiempo de envío (ms):").grid(row=2, column=0, padx=10, pady=10)
        self.send_interval_entry = tk.Entry(self)
        self.send_interval_entry.grid(row=2, column=1, padx=10, pady=10)

        # Botón para guardar la configuración
        self.save_button = tk.Button(self, text="Guardar", command=self.save_config)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def save_config(self):
        # Obtener los valores de las entradas
        port = self.port_entry.get()
        well_name = self.well_name_entry.get()
        send_interval = self.send_interval_entry.get()

        # Aquí puedes agregar el código para guardar la configuración
        print(f"Puerto: {port}, Nombre del pozo: {well_name}, Tiempo de envío: {send_interval}")

        # Cerrar la ventana después de guardar
        self.main.destroy()
