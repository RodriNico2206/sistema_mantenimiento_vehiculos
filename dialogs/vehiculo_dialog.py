# dialogs/vehiculo_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox


class VehiculoDialog:
    def __init__(self, parent, app, callback, vehiculo_data=None):
        self.app = app
        self.callback = callback
        self.vehiculo_data = vehiculo_data

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Agregar Vehículo" if not vehiculo_data else "Editar Vehículo")
        self.dialog.geometry("400x450")
        self.dialog.resizable(False, False)

        # Centrar diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.setup_ui()

    def setup_ui(self):
        # Campos del formulario
        fields = [
            ("Placa:", "placa_entry"),
            ("Marca:", "marca_entry"),
            ("Modelo:", "modelo_entry"),
            ("Año:", "anio_entry"),
            ("Color:", "color_entry"),
            ("VIN:", "vin_entry"),
            ("Kilometraje Actual:", "kilometraje_entry"),
        ]

        self.entries = {}
        for i, (label_text, attr_name) in enumerate(fields):
            ttk.Label(self.dialog, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(self.dialog, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[attr_name] = entry

        # Llenar campos si es edición
        if self.vehiculo_data:
            # vehiculo_data: (id, placa, marca, modelo, anio, color, vin, kilometraje_actual)
            self.entries['placa_entry'].insert(0, self.vehiculo_data[1])
            self.entries['marca_entry'].insert(0, self.vehiculo_data[2])
            self.entries['modelo_entry'].insert(0, self.vehiculo_data[3])
            if self.vehiculo_data[4]:
                self.entries['anio_entry'].insert(0, str(self.vehiculo_data[4]))
            self.entries['color_entry'].insert(0, self.vehiculo_data[5] or "")
            self.entries['vin_entry'].insert(0, self.vehiculo_data[6] or "")
            self.entries['kilometraje_entry'].insert(0, str(self.vehiculo_data[7] or 0))

        # Botones
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Guardar", command=self.guardar_vehiculo).pack(side='right', padx=10)

        self.entries['placa_entry'].focus()

    def guardar_vehiculo(self):
        placa = self.entries['placa_entry'].get().strip().upper()
        marca = self.entries['marca_entry'].get().strip()
        modelo = self.entries['modelo_entry'].get().strip()
        anio_str = self.entries['anio_entry'].get().strip()
        color = self.entries['color_entry'].get().strip()
        vin = self.entries['vin_entry'].get().strip()
        kilometraje_str = self.entries['kilometraje_entry'].get().strip()

        if not placa or not marca or not modelo:
            messagebox.showerror("Error", "Placa, Marca y Modelo son obligatorios")
            return

        # Validar año
        anio = None
        if anio_str:
            try:
                anio = int(anio_str)
            except ValueError:
                messagebox.showerror("Error", "El año debe ser un número válido")
                return

        # Validar kilometraje
        kilometraje = 0
        if kilometraje_str:
            try:
                kilometraje = int(kilometraje_str)
            except ValueError:
                messagebox.showerror("Error", "El kilometraje debe ser un número válido")
                return

        try:
            if self.vehiculo_data:  # Edición
                self.app.get_db().execute_query(
                    """UPDATE vehiculos SET placa=?, marca=?, modelo=?, anio=?, color=?, vin=?, kilometraje_actual=?
                       WHERE id=?""",
                    (placa, marca, modelo, anio, color, vin, kilometraje, self.vehiculo_data[0])
                )
            else:  # Inserción
                self.app.get_db().execute_query(
                    """INSERT INTO vehiculos (placa, marca, modelo, anio, color, vin, kilometraje_actual)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (placa, marca, modelo, anio, color, vin, kilometraje)
                )

            self.callback()
            self.dialog.destroy()
            messagebox.showinfo("Éxito", "Vehículo guardado correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar vehículo: {str(e)}")
