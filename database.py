import sqlite3, hashlib, os, sys
from datetime import datetime

def obtener_ruta_db():
    """Obtiene la ruta correcta para la base de datos.
    
    Cuando la app está empaquetada con PyInstaller, usa el directorio
    donde está el ejecutable. En modo desarrollo, usa el directorio actual.
    """
    if getattr(sys, 'frozen', False):
        # Ejecutando como ejecutable empaquetado
        directorio_ejecutable = os.path.dirname(sys.executable)
    else:
        # Ejecutando en modo desarrollo
        directorio_ejecutable = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(directorio_ejecutable, "mantenimiento_vehiculos.db")


class Database:
    def __init__(self, db_name=None):
        if db_name is None:
            db_name = obtener_ruta_db()
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Tabla de usuarios
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL,
            email TEXT,
            rol TEXT DEFAULT 'usuario',  -- 'admin' o 'usuario'
            activo INTEGER DEFAULT 1,
            fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """
        )

        # Tabla de vehículos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                placa TEXT UNIQUE NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                anio INTEGER,
                color TEXT,
                vin TEXT,
                kilometraje_actual INTEGER DEFAULT 0,
                fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabla de servicios / mantenimientos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS servicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehiculo_id INTEGER NOT NULL,
                fecha_servicio TEXT NOT NULL,
                tipo_servicio TEXT NOT NULL,
                descripcion TEXT,
                kilometraje_aplicado INTEGER NOT NULL,
                kilometraje_proximo_servicio INTEGER NOT NULL,
                costo REAL DEFAULT 0,
                taller TEXT,
                notas TEXT,
                FOREIGN KEY (vehiculo_id) REFERENCES vehiculos (id)
            )
        ''')

        # Tabla de configuración
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alerta_km_anticipacion INTEGER DEFAULT 500
            )
        ''')

        # Insertar configuración por defecto si no existe
        cursor.execute("SELECT COUNT(*) FROM configuracion")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO configuracion (alerta_km_anticipacion) VALUES (?)",
                (500,)
            )

        # Insertar usuario admin por defecto si no existe
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            password_hash = self.hash_password("admin123")
            cursor.execute(
                "INSERT INTO usuarios (username, password, nombre, email, rol) VALUES (?, ?, ?, ?, ?)",
                ("admin", password_hash, "Administrador", "admin@empresa.com", "admin")
            )

        self.conn.commit()

    def hash_password(self, password):
        """Encripta la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verificar_usuario(self, username, password):
        """Verifica las credenciales del usuario y devuelve información completa"""
        cursor = self.conn.cursor()
        password_hash = self.hash_password(password)
        
        cursor.execute(
            "SELECT id, username, nombre, email, rol, activo FROM usuarios WHERE username = ? AND password = ? AND activo = 1",
            (username, password_hash)
        )
        
        return cursor.fetchone()

    def obtener_usuario_por_id(self, usuario_id):
        """Obtiene la información completa de un usuario por su ID"""
        return self.fetch_one("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))

    def execute_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    def fetch_all(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    def verificar_permisos_administrador(self, usuario_id):
        """Verifica si un usuario tiene permisos de administrador"""
        usuario = self.obtener_usuario_por_id(usuario_id)
        return usuario and usuario[5] == 'admin'  # índice 5 = rol

    def puede_crear_usuario(self, usuario_id):
        """Verifica si un usuario puede crear otros usuarios"""
        return self.verificar_permisos_administrador(usuario_id)

    def puede_editar_usuario(self, usuario_id, target_usuario_id):
        """Verifica permisos para editar usuarios"""
        if self.verificar_permisos_administrador(usuario_id):
            return True
        return usuario_id == target_usuario_id
