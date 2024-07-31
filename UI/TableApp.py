import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pandas as pd
import json

class TableApp(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main = self.master
        self.main.geometry('600x400+200+100')
        self.main.title('Tabla de Sensores')

        self.frame = tk.Frame(self.main)
        self.frame.pack(fill='both', expand=True)

        # Cargar datos desde JSON
        self.data = self.load_sensors()

        # Crear la tabla
        self.create_table()

        # Botón para añadir una nueva fila
        self.add_row_button = tk.Button(self.main, text="Añadir Fila", command=self.add_new_row)
        self.add_row_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Botón para borrar la fila seleccionada
        self.delete_row_button = tk.Button(self.main, text="Borrar Fila", command=self.delete_selected_row)
        self.delete_row_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Botón para guardar los cambios
        self.save_button = tk.Button(self.main, text="Guardar Cambios", command=self.save_changes)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

    def load_sensors(self, filename="sensors.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                return pd.DataFrame(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return pd.DataFrame({'IP': [], 'Port': [], 'WITSID': []})

    def save_sensors(self, data, filename="sensors.json"):
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error al guardar datos en JSON: {e}")

    def create_table(self):
        self.tree = ttk.Treeview(self.frame, columns=('IP', 'Port', 'WITSID'), show='headings')
        self.tree.heading('IP', text='IP')
        self.tree.heading('Port', text='Port')
        self.tree.heading('WITSID', text='WITSID')
        self.tree.pack(fill='both', expand=True)

        # Añadir datos a la tabla
        for index, row in self.data.iterrows():
            self.tree.insert("", "end", values=(row['IP'], row['Port'], row['WITSID']))

        # Doble clic para editar
        self.tree.bind('<Double-1>', self.on_double_click)

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        col = self.tree.identify_column(event.x)
        col_number = int(col.replace('#', '')) - 1
        col_name = self.tree['columns'][col_number]

        old_value = self.tree.item(item, 'values')[col_number]

        new_value = simpledialog.askstring("Input", f"Nuevo valor para {col_name}:", initialvalue=old_value)
        if new_value:
            current_values = list(self.tree.item(item, 'values'))
            current_values[col_number] = new_value
            self.tree.item(item, values=current_values)

    def add_new_row(self):
        self.tree.insert("", "end", values=("", "", ""))

    def delete_selected_row(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)

    def save_changes(self):
        # Extraer datos del Treeview y guardar en DataFrame
        rows = []
        for row in self.tree.get_children():
            values = self.tree.item(row)["values"]
            rows.append({'IP': values[0], 'Port': values[1], 'WITSID': values[2]})

        df = pd.DataFrame(rows)
        self.save_sensors(df.to_dict('records'))
        messagebox.showinfo("Guardar", "Cambios guardados exitosamente en JSON")


if __name__ == '__main__':
    app = tk.Tk()
    test = TableApp(app)
    test.pack(fill='both', expand=True)
    app.mainloop()
