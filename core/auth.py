"""
Sistema de autenticación de usuarios - SIN LICENCIA
"""
import os
import hashlib
from datetime import datetime

class Autenticacion:
    """Sistema de autenticación de usuarios con hash"""
    
    @staticmethod
    def _hash_password(password):
        """Genera hash SHA-256 de una contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verificar_credenciales(usuario, contrasena):
        """Verifica las credenciales del usuario con hash"""
        from .database import Database
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Calcular hash de la contraseña ingresada
            hash_ingresado = Autenticacion._hash_password(contrasena)
            
            cursor.execute(
                "SELECT * FROM usuarios WHERE usuario = ? AND contrasena_hash = ? AND activo = 1",
                (usuario, hash_ingresado)
            )
            resultado = cursor.fetchone()
            conn.close()
            return resultado
        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
            return None
    
    @staticmethod
    def cambiar_contrasena(usuario, nueva_contrasena):
        """Cambia la contraseña de un usuario (con hash)"""
        from .database import Database
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            nuevo_hash = Autenticacion._hash_password(nueva_contrasena)
            cursor.execute(
                "UPDATE usuarios SET contrasena_hash = ? WHERE usuario = ?",
                (nuevo_hash, usuario)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al cambiar contraseña: {e}")
            return False
    
    @staticmethod
    def restaurar_contrasena(usuario):
        """Restaura la contraseña por defecto (con hash)"""
        from .database import Database
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            # Restaurar a "123456" con hash
            hash_default = Autenticacion._hash_password("123456")
            cursor.execute(
                "UPDATE usuarios SET contrasena_hash = ? WHERE usuario = ?",
                (hash_default, usuario)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al restaurar contraseña: {e}")
            return False
    
    @staticmethod
    def obtener_usuarios():
        """Obtiene todos los usuarios"""
        from .database import Database
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, usuario, rol, nombre_completo, fecha_registro, activo FROM usuarios")
            resultados = cursor.fetchall()
            conn.close()
            return resultados
        except:
            return []
    
    @staticmethod
    def crear_usuario(usuario, contrasena, rol, nombre_completo):
        """Crea un nuevo usuario (con hash)"""
        from .database import Database
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            hash_pass = Autenticacion._hash_password(contrasena)
            cursor.execute('''
                INSERT INTO usuarios (usuario, contrasena_hash, rol, nombre_completo, fecha_registro, activo)
                VALUES (?, ?, ?, ?, ?, 1)
            ''', (usuario, hash_pass, rol, nombre_completo, datetime.now().strftime("%d/%m/%Y")))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return False
    
    @staticmethod
    def desactivar_usuario(usuario_id):
        """Desactiva un usuario"""
        from .database import Database
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET activo = 0 WHERE id = ?", (usuario_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al desactivar usuario: {e}")
            return False