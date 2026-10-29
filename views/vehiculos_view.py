# views/vehiculos_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from dialogs.vehiculo_dialog import VehiculoDialog
from utils.excel_utils import ExcelUtils


class VehiculosView:
    def __init__(self, parent, app):
        self.app = app
        self.frame = ttk.Frame(parent)
        self.setup_ui()

    def setup_ui(self):
        # Treeview para vehículos
        columns = ('id', 'placa', 'marca', 'modelo', 'anio', 'color', 'kilometraje_actual')
        self.vehiculos_tree = ttk.Treeview(self.frame, columns=columns, show='headings')

        for col in columns:
            self.vehiculos_tree.heading(col, text=col.capitalize().replace('_', ' '))
            self.vehiculos_tree.column(col, width=100)

        self.vehiculos_tree.pack(fill='both', expand=True, padx=5, pady=5)

        # Botones para vehículos
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=5)

        # Botones a la izquierda
        left_button_frame = ttk.Frame(button_frame)
        left_button_frame.pack(side='left')

        ttk.Button(left_button_frame, text="Agregar Vehículo", command=self.agregar_vehiculo).pack(side='left', padx=5)
        ttk.Button(left_button_frame, text="Editar Vehículo", command=self.editar_vehiculo).pack(side='left', padx=5)
        ttk.Button(left_button_frame, text="Eliminar Vehículo", command=self.eliminar_vehiculo).pack(side='left', padx=5)

        # Botones a la derecha (Importación/Exportación)
        right_button_frame = ttk.Frame(button_frame)
        right_button_frame.pack(side='right')

        ttk.Button(right_button_frame, text="Exportar a Excel",
                   command=self.exportar_vehiculos_excel).pack(side='right', padx=5)
        ttk.Button(right_button_frame, text="Importar desde Excel",
                   command=self.importar_vehiculos_excel).pack(side='right', padx=5)

    def load_vehiculos(self):
        # Cargar vehículos en el treeview
        vehiculos = self.app.get_db().fetch_all(
            "SELECT id, placa, marca, modelo, anio, color, kilometraje_actual FROM vehiculos ORDER BY placa"
        )

        # Limpiar treeview
        for item in self.vehiculos_tree.get_children():
            self.vehiculos_tree.delete(item)

        # Insertar vehículos
        for vehiculo in vehiculos:
            self.vehiculos_tree.insert('', 'end', values=vehiculo)

        # Actualizar combobox en servicios si existe
        if hasattr(self.app, 'servicios_view'):
            self.app.servicios_view.actualizar_vehiculos_combobox()

    def agregar_vehiculo(self):
        VehiculoDialog(self.frame, self.app, self.load_vehiculos)

    def editar_vehiculo(self):
        selection = self.vehiculos_tree.selection()
        if selection:
            item = self.vehiculos_tree.item(selection[0])
            VehiculoDialog(self.frame, self.app, self.load_vehiculos, item['values'])
        else:
            messagebox.showerror("Error", "Seleccione un vehículo para editar")

    def eliminar_vehiculo(self):
        selection = self.vehiculos_tree.selection()
        if selection:
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este vehículo?\nEsto eliminará también todos sus servicios registrados."):
                item = self.vehiculos_tree.item(selection[0])
                try:
                    # Primero eliminar servicios asociados
                    self.app.get_db().execute_query("DELETE FROM servicios WHERE vehiculo_id = ?", (item['values'][0],))
                    # Luego eliminar el vehículo
                    self.app.get_db().execute_query("DELETE FROM vehiculos WHERE id = ?", (item['values'][0],))
                    self.load_vehiculos()
                    messagebox.showinfo("Éxito", "Vehículo eliminado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar vehículo: {str(e)}")
        else:
            messagebox.showerror("Error", "Seleccione un vehículo para eliminar")

    def exportar_vehiculos_excel(self):
        ExcelUtils.exportar_vehiculos_excel(self.app.get_db())

    def importar_vehiculos_excel(self):
        ExcelUtils.importar_vehiculos_excel(self.app.get_db(), self.load_vehiculos)
