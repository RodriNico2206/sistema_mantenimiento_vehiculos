# utils/excel_utils.py
import csv
from datetime import datetime


class ExcelUtils:
    @staticmethod
    def exportar_vehiculos_excel(db):
        """Exporta vehículos a un archivo CSV (formato compatible con Excel)"""
        try:
            from tkinter import filedialog, messagebox
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Exportar Vehículos"
            )
            if not filepath:
                return

            vehiculos = db.fetch_all(
                "SELECT id, placa, marca, modelo, anio, color, vin, kilometraje_actual, fecha_registro FROM vehiculos ORDER BY placa"
            )

            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Placa', 'Marca', 'Modelo', 'Año', 'Color', 'VIN', 'Kilometraje Actual', 'Fecha Registro'])
                for v in vehiculos:
                    writer.writerow(v)

            messagebox.showinfo("Éxito", f"Vehículos exportados correctamente a:\n{filepath}")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")

    @staticmethod
    def importar_vehiculos_excel(db, callback):
        """Importa vehículos desde un archivo CSV"""
        try:
            from tkinter import filedialog, messagebox
            filepath = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Importar Vehículos"
            )
            if not filepath:
                return

            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # Saltar encabezado
                count = 0
                for row in reader:
                    if len(row) >= 7:
                        placa = row[1].strip().upper() if len(row) > 1 else ""
                        marca = row[2].strip() if len(row) > 2 else ""
                        modelo = row[3].strip() if len(row) > 3 else ""
                        anio = int(row[4]) if len(row) > 4 and row[4].strip().isdigit() else None
                        color = row[5].strip() if len(row) > 5 else ""
                        vin = row[6].strip() if len(row) > 6 else ""
                        kilometraje = int(row[7]) if len(row) > 7 and row[7].strip().isdigit() else 0

                        if placa and marca and modelo:
                            db.execute_query(
                                "INSERT INTO vehiculos (placa, marca, modelo, anio, color, vin, kilometraje_actual) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (placa, marca, modelo, anio, color, vin, kilometraje)
                            )
                            count += 1

            callback()
            messagebox.showinfo("Éxito", f"Se importaron {count} vehículos correctamente")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al importar: {str(e)}")
