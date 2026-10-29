# dialogs/servicio_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class ServicioDialog:
    def __init__(self, parent, app, callback, vehiculo_id, servicio_data=None):
        self.app = app
        self.callback = callback
        self.vehiculo_id = vehiculo_id
        self.servicio_data = servicio_data

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuevo Servicio" if not servicio_data else "Editar Servicio")
        self.dialog.geometry("450x550")
        self.dialog.resizable(False, False)

        # Centrar diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.setup_ui()

    def setup_ui(self):
        # Campos del formulario
        fields = [
            ("Fecha del Servicio:", "fecha_entry", datetime.now().strftime("%Y-%m-%d")),
            ("Tipo de Servicio:", "tipo_entry", ""),
            ("Descripción:", "descripcion_entry", ""),
            ("Kilometraje al aplicar servicio:", "km_aplicado_entry", ""),
            ("Kilometraje próximo servicio:", "km_proximo_entry", ""),
            ("Costo:", "costo_entry", "0"),
            ("Taller:", "taller_entry", ""),
            ("Notas:", "notas_entry", ""),
        ]

        self.entries = {}
        for i, (label_text, attr_name, default_value) in enumerate(fields):
            ttk.Label(self.dialog, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            if attr_name == "notas_entry":
                entry = tk.Text(self.dialog, width=30, height=3)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entry.insert("1.0", default_value)
            else:
                entry = ttk.Entry(self.dialog, width=30)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entry.insert(0, default_value)
            self.entries[attr_name] = entry

        # Llenar campos si es edición
        if self.servicio_data:
            # servicio_data: (id, fecha_servicio, tipo_servicio, descripcion, kilometraje_aplicado,
            #               kilometraje_proximo_servicio, costo, taller, notas)
            self.entries['fecha_entry'].delete(0, tk.END)
            self.entries['fecha_entry'].insert(0, self.servicio_data[1])
            self.entries['tipo_entry'].delete(0, tk.END)
            self.entries['tipo_entry'].insert(0, self.servicio_data[2] or "")
            self.entries['descripcion_entry'].delete(0, tk.END)
            self.entries['descripcion_entry'].insert(0, self.servicio_data[3] or "")
            self.entries['km_aplicado_entry'].delete(0, tk.END)
            self.entries['km_aplicado_entry'].insert(0, str(self.servicio_data[4] or 0))
            self.entries['km_proximo_entry'].delete(0, tk.END)
            self.entries['km_proximo_entry'].insert(0, str(self.servicio_data[5] or 0))
            self.entries['costo_entry'].delete(0, tk.END)
            self.entries['costo_entry'].insert(0, str(self.servicio_data[6] or 0))
            self.entries['taller_entry'].delete(0, tk.END)
            self.entries['taller_entry'].insert(0, self.servicio_data[7] or "")
            self.entries['notas_entry'].delete("1.0", tk.END)
            self.entries['notas_entry'].insert("1.0", self.servicio_data[8] or "")

        # Botones
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Guardar", command=self.guardar_servicio).pack(side='right', padx=10)

        self.entries['tipo_entry'].focus()

    def guardar_servicio(self):
        fecha = self.entries['fecha_entry'].get().strip()
        tipo_servicio = self.entries['tipo_entry'].get().strip()
        descripcion = self.entries['descripcion_entry'].get().strip()
        km_aplicado_str = self.entries['km_aplicado_entry'].get().strip()
        km_proximo_str = self.entries['km_proximo_entry'].get().strip()
        costo_str = self.entries['costo_entry'].get().strip()
        taller = self.entries['taller_entry'].get().strip()
        notas = self.entries['notas_entry'].get("1.0", tk.END).strip()

        if not fecha or not tipo_servicio:
            messagebox.showerror("Error", "Fecha y Tipo de Servicio son obligatorios")
            return

        # Validar fecha
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "La fecha debe tener formato YYYY-MM-DD")
            return

        # Validar kilometraje aplicado
        try:
            km_aplicado = int(km_aplicado_str) if km_aplicado_str else 0
        except ValueError:
            messagebox.showerror("Error", "El kilometraje aplicado debe ser un número válido")
            return

        # Validar kilometraje próximo servicio
        try:
            km_proximo = int(km_proximo_str) if km_proximo_str else 0
        except ValueError:
            messagebox.showerror("Error", "El kilometraje de próximo servicio debe ser un número válido")
            return

        # Validar costo
        try:
            costo = float(costo_str) if costo_str else 0.0
        except ValueError:
            messagebox.showerror("Error", "El costo debe ser un número válido")
            return

        try:
            if self.servicio_data:  # Edición
                self.app.get_db().execute_query(
                    """UPDATE servicios SET fecha_servicio=?, tipo_servicio=?, descripcion=?,
                                                  kilometraje_aplicado=?, kilometraje_proximo_servicio=?,
                                                  costo=?, taller=?, notas=?
                                                    WHERE id=?""",
                    (fecha, tipo_servicio, descripcion, km_aplicado, km_proximo,
                     costo, taller, notas, self.servicio_data[0])
                )
            else:  # Inserción
                self.app.get_db().execute_query(
                    """INSERT INTO servicios (vehiculo_id, fecha_servicio, tipo_servicio, descripcion,
                                              kilometraje_aplicado, kilometraje_proximo_servicio,
                                              costo, taller, notas)
                                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (self.vehiculo_id, fecha, tipo_servicio, descripcion, km_aplicado, km_proximo,
                     costo, taller, notas)
                )
                # Actualizar kilometraje actual del vehículo al kilometraje aplicado del servicio
                self.app.get_db().execute_query(
                    "UPDATE vehiculos SET kilometraje_actual = ? WHERE id = ?",
                    (km_aplicado, self.vehiculo_id)
                )

            self.callback()
            self.dialog.destroy()
            messagebox.showinfo("Éxito", "Servicio guardado correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar servicio: {str(e)}")
