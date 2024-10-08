import tkinter as tk
from UI.HomeApp import HomeApp
from UI.TableApp import TableApp
from UI.WitsConfig import WitsConfig
class MainApp(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main = self.master
        self.main.geometry('800x600+200+100')
        self.main.title('Home')

        self.create_menu()
        self.create_home()

    def create_menu(self):
        menubar = tk.Menu(self.main)
        self.main.config(menu=menubar)

        # Configuración del menú
        config_menu = tk.Menu(menubar, tearoff=0)
        config_menu.add_command(label="Editar Sensores", command=self.open_table_app)
        config_menu.add_command(label="WITS", command=self.open_wits_config)  # Nueva opción de menú

        menubar.add_cascade(label="Configuración", menu=config_menu)

    def create_home(self):
        self.home_app = HomeApp(self)
        self.home_app.pack(fill='both', expand=True)

    def open_table_app(self):
        self.new_window = tk.Toplevel(self.main)
        self.app = TableApp(self.new_window)

    def open_wits_config(self):
        self.new_window = tk.Toplevel(self.main)
        self.app = WitsConfig(self.new_window)


if __name__ == '__main__':
    root = tk.Tk()
    main_app = MainApp(root)
    main_app.pack(fill='both', expand=True)
    root.mainloop()


#preguntale a josafat
#la idea sería proponer dos software una visualización remota web
#Control local escritorio
#divir 2 presentación unicamente mostrar la visualización

