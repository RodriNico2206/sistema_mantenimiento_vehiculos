# Sistema de Mantenimiento de Vehículos

## Descripción
Aplicación de escritorio para dar seguimiento a los mantenimientos de vehículos (autos), desarrollada con Python y Tkinter,
basada en la arquitectura del repositorio `sistema_facturacion`.

Permite registrar vehículos y cargar los servicios realizados, especificando:
- Servicio realizado
- Kilometraje al cual se aplicó el servicio
- Kilometraje post-servicio (a los cuántos kilómetros será el próximo servicio)

## Características
- Autenticación de usuarios con roles (admin / usuario)
- Gestión de vehículos (alta, edición, eliminación, listado)
- Registro de servicios/mantenimientos por vehículo
- Historial de servicios por vehículo
- Exportación e importación de vehículos a CSV (Excel)
- Base de datos SQLite local (sin configuración adicional)

## Estructura del proyecto
```
sistema_mantenimiento_vehiculos/
├── main.py                 # Punto de entrada principal
├── app.py                  # Clase principal de la aplicación
├── database.py             # Manejo de base de datos SQLite
├── login_window.py         # Ventana de autenticación
├── models.py               # Modelos de datos (dataclasses)
├── models/
│   ├── __init__.py
│   ├── vehiculo.py         # Modelo Vehiculo
│   └── servicio.py         # Modelo Servicio
├── views/
│   ├── __init__.py
│   ├── vehiculos_view.py   # Vista CRUD de vehículos
│   ├── servicios_view.py   # Vista de servicios por vehículo
│   └── historial_view.py   # Vista de historial de servicios
├── dialogs/
│   ├── __init__.py
│   ├── vehiculo_dialog.py  # Diálogo alta/edición vehículo
│   └── servicio_dialog.py  # Diálogo alta/edición servicio
├── utils/
│   ├── __init__.py
│   └── excel_utils.py      # Utilidades CSV/Excel
├── templates/
│   └── reporte_mantenimiento.html  # Plantilla HTML para reportes
├── SistemaMantenimientoVehiculos.spec  # Configuración de PyInstaller
├── build_exe.py            # Script para construir el .exe de Windows
├── requirements.txt        # Dependencias para empaquetado
├── .gitignore              # Archivos ignorados por Git
└── README.md               # Este archivo
```

## Requisitos
- Python 3.x
- Tkinter (incluido en la instalación estándar de Python)

## Instalación y ejecución (modo desarrollo)
```bash
# Clonar o crear el proyecto
cd sistema_mantenimiento_vehiculos

# Ejecutar la aplicación
python main.py
```

## Crear ejecutable de Windows (.exe)

Para distribuir la aplicación como un ejecutable de Windows sin necesidad de tener Python instalado:

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Construir el ejecutable
```bash
python build_exe.py
```

Esto generará el archivo `dist/SistemaMantenimientoVehiculos.exe`.

### 3. Distribuir
El archivo `.exe` en la carpeta `dist/` se puede ejecutar en cualquier Windows sin instalar Python. La base de datos SQLite se creará automáticamente junto al ejecutable la primera vez que se inicie.

**Nota:** El archivo `.exe` no requiere instalación, simplemente haz doble clic para ejecutarlo.

## Credenciales por defecto
- Usuario: `admin`
- Contraseña: `admin123`

## Flujo de uso
1. Iniciar sesión con las credenciales
2. En la pestaña **Vehículos**, registrar el(auto) (placa, marca, modelo, año, color, VIN, kilometraje actual)
3. En la pestaña **Servicios**, seleccionar un vehículo y cargar un nuevo servicio:
   - Tipo de servicio (ej. Cambio de aceite, Revisión, Frenos)
   - Kilometraje al cual se aplicó el servicio
   - Kilometraje post-servicio (próximo servicio)
   - Costo, taller, notas, etc.
4. En la pestaña **Historial**, ver todos los servicios de un vehículo seleccionado
