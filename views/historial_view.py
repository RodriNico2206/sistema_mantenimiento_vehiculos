# views/historial_view.py
import tkinter as tk
from tkinter import ttk, messagebox


class HistorialView:
    def __init__(self, parent, app):
        self.app = app
        self.frame = ttk.Frame(parent)
        self.setup_ui()

    def setup_ui(self):
        # Frame superior: selección de vehículo
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(top_frame, text="Seleccionar Vehículo:").pack(side='left', padx=(0, 5))
        self.vehiculo_combobox = ttk.Combobox(top_frame, state="readonly", width=40)
        self.vehiculo_combobox.pack(side='left', padx=(0, 10))
        self.vehiculo_combobox.bind('<<ComboboxSelected>>', self.on_vehiculo_seleccionado)

        ttk.Button(top_frame, text="Ver Historial", command=self.cargar_historial).pack(side='left')

        # Treeview para historial de servicios
        columns = ('fecha_servicio', 'tipo_servicio', 'descripcion', 'kilometraje_aplicado', 'kilometraje_proximo_servicio', 'costo', 'taller')
        self.historial_tree = ttk.Treeview(self.frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.historial_tree.heading(col, text=col.capitalize().replace('_', ' '))
            self.historial_tree.column(col, width=120)

        self.historial_tree.pack(fill='both', expand=True, padx=5, pady=5)

        # Resumen del vehículo
        self.resumen_var = tk.StringVar(value="Seleccione un vehículo")
        ttk.Label(self.frame, textvariable=self.resumen_var, font=('Arial', 10, 'bold')).pack(padx=10, pady=5)

        self.vehiculo_seleccionado_id = None

    def actualizar_vehiculos_combobox(self):
        """Actualiza el combobox de vehículos desde la base de datos"""
        vehiculos = self.app.get_db().fetch_all(
            "SELECT id, placa, marca, modelo, kilometraje_actual FROM vehiculos ORDER BY placa"
        )
        self.vehiculos_data = vehiculos
        self.vehiculo_combobox['values'] = [f"{v[1]} - {v[2]} {v[3]} (KM: {v[4]})" for v in vehiculos]

    def on_vehiculo_seleccionado(self, event):
        """Cuando se selecciona un vehículo en el combobox"""
        selection = self.vehiculo_combobox.current()
        if selection >= 0 and hasattr(self, 'vehiculos_data'):
            vehiculo = self.vehiculos_data[selection]
            self.vehiculo_seleccionado_id = vehiculo[0]
            self.resumen_var.set(
                f"Placa: {vehiculo[1]} | {vehiculo[2]} {vehiculo[3]} | Kilometraje actual: {vehiculo[4]} km"
            )

    def cargar_historial(self):
        """Carga el historial de servicios del vehículo seleccionado"""
        if self.vehiculo_seleccionado_id is None:
            messagebox.showerror("Error", "Seleccione un vehículo primero")
            return

        # Obtener datos del vehículo
        vehiculo = self.app.get_db().fetch_one(
            "SELECT placa, marca, modelo, kilometraje_actual FROM vehiculos WHERE id = ?",
            (self.vehiculo_seleccionado_id,)
        )
        if vehiculo:
            self.resumen_var.set(
                f"Placa: {vehiculo[0]} | {vehiculo[1]} {vehiculo[2]} | Kilometraje actual: {vehiculo[3]} km"
            )

        # Obtener historial de servicios
        servicios = self.app.get_db().fetch_all(
            """SELECT fecha_servicio, tipo_servicio, descripcion, kilometraje_aplicado,
                          kilometraje_proximo_servicio, costo, taller
                   FROM servicios
                   WHERE vehiculo_id = ?
                   ORDER BY fecha_servicio DESC""",
            (self.vehiculo_seleccionado_id,)
        )

        # Limpiar treeview
        for item in self.historial_tree.get_children():
            self.historial_tree.delete(item)

        # Insertar servicios
        for servicio in servicios:
            self.historial_tree.insert('', 'end', values=servicio)

        if not servicios:
            messagebox.showinfo("Información", "Este vehículo no tiene servicios registrados")
