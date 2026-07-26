"""
Modelo para la gestión de préstamos
"""
from datetime import datetime, timedelta
from core.database import Database

class Prestamo:
    """Modelo de préstamo de expediente"""
    
    def __init__(self, id_expediente=None, solicitado_por="", area="", 
                 motivo="", fecha_prestamo=None, fecha_limite=None):
        self.id_expediente = id_expediente
        self.solicitado_por = solicitado_por
        self.area = area
        self.motivo = motivo
        self.fecha_prestamo = fecha_prestamo or datetime.now().strftime("%d/%m/%Y")
        self.fecha_limite = fecha_limite or (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        self.fecha_devolucion_real = None
        self.devuelto_por = None
        self.estado = "Activo"
    
    def guardar(self):
        """Guarda el préstamo en la base de datos"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO prestamos 
            (id_expediente, solicitado_por, area, motivo, fecha_prestamo, 
             fecha_limite_devolucion, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.id_expediente, self.solicitado_por, self.area, self.motivo,
              self.fecha_prestamo, self.fecha_limite, self.estado))
        
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.id
    
    @staticmethod
    def obtener_activo_por_expediente(id_expediente):
        """Obtiene el préstamo activo de un expediente"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM prestamos WHERE id_expediente = ? AND estado = 'Activo'",
            (id_expediente,)
        )
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    
    @staticmethod
    def registrar_devolucion(id_prestamo, fecha_devolucion, devuelto_por):
        """Registra la devolución de un préstamo"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE prestamos 
            SET fecha_devolucion_real = ?, devuelto_por = ?, estado = 'Devuelto'
            WHERE id = ?
        ''', (fecha_devolucion, devuelto_por, id_prestamo))
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def obtener_todos_activos():
        """Obtiene todos los préstamos activos"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, e.numero_expediente, e.nombre, e.apellido_paterno, e.apellido_materno
            FROM prestamos p
            JOIN expedientes e ON p.id_expediente = e.id
            WHERE p.estado = 'Activo'
            ORDER BY p.fecha_prestamo DESC
        ''')
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    
    @staticmethod
    def obtener_vencidos():
        """Obtiene los préstamos vencidos"""
        hoy = datetime.now()
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, e.numero_expediente, e.nombre, e.apellido_paterno, e.apellido_materno
            FROM prestamos p
            JOIN expedientes e ON p.id_expediente = e.id
            WHERE p.estado = 'Activo'
        ''')
        resultados = cursor.fetchall()
        
        vencidos = []
        for r in resultados:
            try:
                fecha_limite = datetime.strptime(r[6], "%d/%m/%Y")
                if fecha_limite < hoy:
                    vencidos.append(r)
            except:
                pass
        
        conn.close()
        return vencidos
    
    @staticmethod
    def contar_por_mes(desde, hasta):
        """Cuenta préstamos por mes"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT strftime('%m/%Y', fecha_prestamo) as mes, COUNT(*) as total
            FROM prestamos
            WHERE fecha_prestamo >= ? AND fecha_prestamo <= ?
            GROUP BY mes
            ORDER BY mes DESC
        ''', (desde, hasta))
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    
    @staticmethod
    def contar_por_area():
        """Cuenta préstamos por área"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT area, COUNT(*) as total
            FROM prestamos
            GROUP BY area
            ORDER BY total DESC
        ''')
        resultados = cursor.fetchall()
        conn.close()
        return resultados