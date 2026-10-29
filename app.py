# app.py
from tkinter import ttk
from database import Database
from views.vehiculos_view import VehiculosView
from views.servicios_view import ServiciosView
from views.historial_view import HistorialView


class MantenimientoApp:
    def __init__(self, root, usuario_actual=None):
        self.root = root
        self.root.title("Sistema de Mantenimiento de Vehículos")
        self.root.geometry("1200x700")

        self.db = Database()
        self.usuario_actual = usuario_actual  # Almacenar usuario actual

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Crear las vistas para cada pestaña
        self.vehiculos_view = VehiculosView(self.notebook, self)
        self.servicios_view = ServiciosView(self.notebook, self)
        self.historial_view = HistorialView(self.notebook, self)

        # Añadir las pestañas
        self.notebook.add(self.vehiculos_view.frame, text="Vehículos")
        self.notebook.add(self.servicios_view.frame, text="Servicios")
        self.notebook.add(self.historial_view.frame, text="Historial")

        # Mostrar información del usuario en la barra de título
        self.actualizar_titulo_ventana()

    def es_administrador(self):
        """Verifica si el usuario actual es administrador"""
        return self.usuario_actual and self.usuario_actual[5] == 'admin'  # índice 5 = rol

    def actualizar_titulo_ventana(self):
        """Actualiza el título de la ventana con información del usuario"""
        if self.usuario_actual:
            nombre = self.usuario_actual[3]  # índice 3 = nombre
            rol = self.usuario_actual[5]     # índice 5 = rol
            self.root.title(f"Sistema de Mantenimiento de Vehículos - {nombre} ({rol})")
        else:
            self.root.title("Sistema de Mantenimiento de Vehículos")

    def load_data(self):
        self.vehiculos_view.load_vehiculos()
        self.servicios_view.actualizar_vehiculos_combobox()
        self.historial_view.actualizar_vehiculos_combobox()

    # Métodos de utilidad que pueden ser accedidos desde las vistas
    def get_db(self):
        return self.db
