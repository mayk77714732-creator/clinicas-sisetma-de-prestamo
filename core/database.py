"""
Gestión de la base de datos SQLite - SIN CURP
"""
import sqlite3
import hashlib
from datetime import datetime
from .config import DB_PATH

class Database:
    """Clase para manejar la conexión y operaciones de la base de datos"""
    
    @staticmethod
    def get_connection():
        """Obtiene una conexión a la base de datos"""
        try:
            import os
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            return sqlite3.connect(DB_PATH)
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise
    
    @staticmethod
    def _hash_password(password):
        """Genera hash SHA-256 de una contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def initialize():
        """Inicializa la base de datos con todas las tablas"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Verificar si la tabla usuarios tiene la columna antigua
            cursor.execute("PRAGMA table_info(usuarios)")
            columnas = [col[1] for col in cursor.fetchall()]
            
            if "contrasena" in columnas and "contrasena_hash" not in columnas:
                print("🔧 Migrando base de datos a hash...")
                cursor.execute("ALTER TABLE usuarios ADD COLUMN contrasena_hash TEXT")
                
                cursor.execute("SELECT id, contrasena FROM usuarios")
                usuarios = cursor.fetchall()
                for id_usuario, contrasena in usuarios:
                    if contrasena:
                        hash_pass = Database._hash_password(contrasena)
                        cursor.execute(
                            "UPDATE usuarios SET contrasena_hash = ? WHERE id = ?",
                            (hash_pass, id_usuario)
                        )
                print("✅ Migración completada")
            
            # Tabla de usuarios (con hash)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE,
                    contrasena_hash TEXT,
                    rol TEXT,
                    nombre_completo TEXT,
                    fecha_registro TEXT,
                    activo INTEGER DEFAULT 1
                )
            ''')
            
            # Tabla de expedientes (SIN CURP)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expedientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_expediente INTEGER UNIQUE,
                    nombre TEXT,
                    apellido_paterno TEXT,
                    apellido_materno TEXT,
                    fecha_nacimiento TEXT,
                    sexo TEXT,
                    colonia TEXT,
                    estado TEXT,
                    fecha_creacion TEXT,
                    fecha_actualizacion TEXT
                )
            ''')
            
            # Tabla de préstamos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prestamos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_expediente INTEGER,
                    solicitado_por TEXT,
                    area TEXT,
                    motivo TEXT,
                    fecha_prestamo TEXT,
                    fecha_limite_devolucion TEXT,
                    fecha_devolucion_real TEXT,
                    devuelto_por TEXT,
                    estado TEXT,
                    FOREIGN KEY (id_expediente) REFERENCES expedientes(id)
                )
            ''')
            
            # Tabla de historial
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historial (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_expediente INTEGER,
                    accion TEXT,
                    fecha TEXT,
                    descripcion TEXT,
                    usuario TEXT,
                    FOREIGN KEY (id_expediente) REFERENCES expedientes(id)
                )
            ''')
            
            # Tabla de permisos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS permisos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rol TEXT,
                    modulo TEXT,
                    permiso TEXT
                )
            ''')
            
            # Índices
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_exp_numero ON expedientes(numero_expediente)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_exp_nombre ON expedientes(nombre)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_exp_estado ON expedientes(estado)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_prestamo_estado ON prestamos(estado)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_prestamo_fecha ON prestamos(fecha_prestamo)')
            
            conn.commit()
            conn.close()
            
            Database.cargar_datos_iniciales()
            
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
    
    @staticmethod
    def cargar_datos_iniciales():
        """Carga datos de ejemplo y usuarios iniciales con hash"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            if cursor.fetchone()[0] > 0:
                conn.close()
                return
            
            # Usuarios por defecto
            usuarios = [
                ("admin", "admin123", "Administrador", "Administrador del Sistema"),
                ("archivo", "archivo123", "Personal de Archivo", "Personal de Archivo"),
                ("consulta", "consulta123", "Consulta", "Médico Consulta")
            ]
            
            for usuario in usuarios:
                hash_pass = Database._hash_password(usuario[1])
                cursor.execute('''
                    INSERT INTO usuarios (usuario, contrasena_hash, rol, nombre_completo, fecha_registro)
                    VALUES (?, ?, ?, ?, ?)
                ''', (usuario[0], hash_pass, usuario[2], usuario[3], datetime.now().strftime("%d/%m/%Y")))
            
            # Permisos por defecto
            permisos = [
                ("Administrador", "todos", "todos"),
                ("Personal de Archivo", "registro", "crear,editar"),
                ("Personal de Archivo", "prestamo", "crear,editar"),
                ("Personal de Archivo", "devolucion", "crear,editar"),
                ("Personal de Archivo", "busqueda", "leer"),
                ("Consulta", "busqueda", "leer"),
                ("Consulta", "historial", "leer"),
                ("Consulta", "reportes", "leer")
            ]
            
            for permiso in permisos:
                cursor.execute('''
                    INSERT INTO permisos (rol, modulo, permiso)
                    VALUES (?, ?, ?)
                ''', permiso)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error al cargar datos iniciales: {e}")