"""
Modelo para la gestión del historial
"""
from datetime import datetime
from core.database import Database

class Historial:
    """Modelo de historial de expedientes"""
    
    @staticmethod
    def registrar(id_expediente, accion, descripcion, usuario="Sistema"):
        """Registra una acción en el historial"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        cursor.execute('''
            INSERT INTO historial (id_expediente, accion, fecha, descripcion, usuario)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_expediente, accion, fecha, descripcion, usuario))
        
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def obtener_por_expediente(id_expediente):
        """Obtiene el historial de un expediente"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM historial 
            WHERE id_expediente = ? 
            ORDER BY fecha DESC
        ''', (id_expediente,))
        
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    
    @staticmethod
    def obtener_por_paciente(termino):
        """Obtiene historial por nombre del paciente"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.numero_expediente, e.nombre, e.apellido_paterno, e.apellido_materno,
                   h.fecha, h.accion, h.descripcion
            FROM expedientes e
            JOIN historial h ON e.id = h.id_expediente
            WHERE e.numero_expediente LIKE ? OR e.nombre LIKE ? OR e.apellido_paterno LIKE ?
            ORDER BY h.fecha DESC
        ''', (f'%{termino}%', f'%{termino}%', f'%{termino}%'))
        
        resultados = cursor.fetchall()
        conn.close()
        return resultados