# views/servicios_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from dialogs.servicio_dialog import ServicioDialog


class ServiciosView:
    def __init__(self, parent, app):
        self.app = app
        self.frame = ttk.Frame(parent)
        self.setup_ui()

    def setup_ui(self):
        # Frame superior: selección de vehículo y botón agregar servicio
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(top_frame, text="Seleccionar Vehículo:").pack(side='left', padx=(0, 5))
        self.vehiculo_combobox = ttk.Combobox(top_frame, state="readonly", width=40)
        self.vehiculo_combobox.pack(side='left', padx=(0, 10))
        self.vehiculo_combobox.bind('<<ComboboxSelected>>', self.on_vehiculo_seleccionado)

        ttk.Button(top_frame, text="Nuevo Servicio", command=self.agregar_servicio).pack(side='left')

        # Frame medio: información del vehículo seleccionado
        info_frame = ttk.LabelFrame(self.frame, text="Información del Vehículo")
        info_frame.pack(fill='x', padx=5, pady=5)

        self.info_vehiculo_var = tk.StringVar(value="Seleccione un vehículo")
        ttk.Label(info_frame, textvariable=self.info_vehiculo_var, font=('Arial', 10, 'bold')).pack(padx=10, pady=5)

        # Treeview para servicios del vehículo seleccionado
        columns = ('id', 'fecha_servicio', 'tipo_servicio', 'kilometraje_aplicado', 'kilometraje_proximo_servicio', 'costo', 'taller')
        self.servicios_tree = ttk.Treeview(self.frame, columns=columns, show='headings', height=10)

        for col in columns:
            self.servicios_tree.heading(col, text=col.capitalize().replace('_', ' '))
            self.servicios_tree.column(col, width=100)

        self.servicios_tree.pack(fill='both', expand=True, padx=5, pady=5)

        # Botones de acción para servicios
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=5)

        ttk.Button(button_frame, text="Nuevo Servicio", command=self.agregar_servicio).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Editar Servicio", command=self.editar_servicio).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Eliminar Servicio", command=self.eliminar_servicio).pack(side='left', padx=5)

        self.vehiculo_seleccionado_id = None

    def actualizar_vehiculos_combobox(self):
        """Actualiza el combobox de vehículos desde la base de datos"""
        vehiculos = self.app.get_db().fetch_all(
            "SELECT id, placa, marca, modelo FROM vehiculos ORDER BY placa"
        )
        self.vehiculos_data = vehiculos
        self.vehiculo_combobox['values'] = [f"{v[1]} - {v[2]} {v[3]}" for v in vehiculos]

    def on_vehiculo_seleccionado(self, event):
        """Cuando se selecciona un vehículo en el combobox"""
        selection = self.vehiculo_combobox.current()
        if selection >= 0 and hasattr(self, 'vehiculos_data'):
            vehiculo = self.vehiculos_data[selection]
            self.vehiculo_seleccionado_id = vehiculo[0]
            self.info_vehiculo_var.set(
                f"Placa: {vehiculo[1]} | {vehiculo[2]} {vehiculo[3]}"
            )
            self.cargar_servicios_vehiculo()

    def cargar_servicios_vehiculo(self):
        """Carga los servicios del vehículo seleccionado"""
        if self.vehiculo_seleccionado_id is None:
            return

        servicios = self.app.get_db().fetch_all(
            """SELECT id, fecha_servicio, tipo_servicio, kilometraje_aplicado,
                          kilometraje_proximo_servicio, costo, taller
                   FROM servicios
                   WHERE vehiculo_id = ?
                   ORDER BY fecha_servicio DESC""",
            (self.vehiculo_seleccionado_id,)
        )

        # Limpiar treeview
        for item in self.servicios_tree.get_children():
            self.servicios_tree.delete(item)

        # Insertar servicios
        for servicio in servicios:
            self.servicios_tree.insert('', 'end', values=servicio)

    def agregar_servicio(self):
        if self.vehiculo_seleccionado_id is None:
            messagebox.showerror("Error", "Seleccione un vehículo primero")
            return
        ServicioDialog(self.frame, self.app, self.cargar_servicios_vehiculo, self.vehiculo_seleccionado_id)

    def editar_servicio(self):
        selection = self.servicios_tree.selection()
        if selection:
            item = self.servicios_tree.item(selection[0])
            ServicioDialog(self.frame, self.app, self.cargar_servicios_vehiculo, self.vehiculo_seleccionado_id, item['values'])
        else:
            messagebox.showerror("Error", "Seleccione un servicio para editar")

    def eliminar_servicio(self):
        selection = self.servicios_tree.selection()
        if selection:
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este servicio?"):
                item = self.servicios_tree.item(selection[0])
                try:
                    self.app.get_db().execute_query("DELETE FROM servicios WHERE id = ?", (item['values'][0],))
                    self.cargar_servicios_vehiculo()
                    messagebox.showinfo("Éxito", "Servicio eliminado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar servicio: {str(e)}")
        else:
            messagebox.showerror("Error", "Seleccione un servicio para eliminar")
