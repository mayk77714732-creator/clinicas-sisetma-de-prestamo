"""
Modelo para la gestión de expedientes - SIN CURP
"""
from datetime import datetime
from core.database import Database

class Expediente:
    """Modelo de expediente clínico"""
    
    def __init__(self, id=None, numero=None, nombre="", apellido_p="", apellido_m="",
                 fecha_nac="", sexo="", colonia="", estado="Disponible"):
        self.id = id
        self.numero = numero
        self.nombre = nombre
        self.apellido_paterno = apellido_p
        self.apellido_materno = apellido_m
        self.fecha_nacimiento = fecha_nac
        self.sexo = sexo
        self.colonia = colonia
        self.estado = estado
        self.fecha_creacion = datetime.now().strftime("%d/%m/%Y")
        self.fecha_actualizacion = self.fecha_creacion
    
    def guardar(self):
        """Guarda el expediente en la base de datos"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtener el siguiente número de expediente automático
            cursor.execute("SELECT MAX(numero_expediente) FROM expedientes")
            max_num = cursor.fetchone()[0]
            if max_num is None:
                self.numero = 1
            else:
                self.numero = max_num + 1
            
            cursor.execute('''
                INSERT INTO expedientes 
                (numero_expediente, nombre, apellido_paterno, apellido_materno,
                 fecha_nacimiento, sexo, colonia, estado, fecha_creacion, fecha_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.numero, self.nombre, self.apellido_paterno, self.apellido_materno,
                  self.fecha_nacimiento, self.sexo, self.colonia, self.estado,
                  self.fecha_creacion, self.fecha_actualizacion))
            
            self.id = cursor.lastrowid
            conn.commit()
            conn.close()
            return self.id
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def obtener_por_id(id_expediente):
        """Obtiene un expediente por su ID"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expedientes WHERE id = ?", (id_expediente,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    
    @staticmethod
    def obtener_por_numero(numero):
        """Obtiene un expediente por su número"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expedientes WHERE numero_expediente = ?", (numero,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    
    @staticmethod
    def buscar(termino, filtro_estado="Todos", limite=100):
        """Busca expedientes por término con límite para rendimiento"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        # Primero buscar por número exacto (más rápido)
        try:
            numero = int(termino)
            cursor.execute(
                "SELECT * FROM expedientes WHERE numero_expediente = ?",
                (numero,)
            )
            resultado = cursor.fetchall()
            if resultado:
                conn.close()
                return resultado
        except:
            pass
        
        # Luego búsqueda general con límite
        query = '''
            SELECT * FROM expedientes 
            WHERE (numero_expediente LIKE ? OR nombre LIKE ? OR apellido_paterno LIKE ? 
                   OR apellido_materno LIKE ?)
        '''
        params = [f'%{termino}%', f'%{termino}%', f'%{termino}%', f'%{termino}%']
        
        if filtro_estado != "Todos":
            query += " AND estado = ?"
            params.append(filtro_estado)
        
        query += " ORDER BY nombre ASC LIMIT ?"
        params.append(limite)
        
        cursor.execute(query, tuple(params))
        resultados = cursor.fetchall()
        
        if len(resultados) == limite:
            print(f"⚠️ Búsqueda limitada a {limite} resultados. Refine su búsqueda.")
        
        conn.close()
        return resultados
    
    @staticmethod
    def obtener_paginado(filtro_estado="Todos", pagina=1, por_pagina=50):
        """Obtiene expedientes con paginación para listas grandes"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        offset = (pagina - 1) * por_pagina
        
        query = "SELECT * FROM expedientes"
        params = []
        count_query = "SELECT COUNT(*) FROM expedientes"
        count_params = []
        
        if filtro_estado != "Todos":
            query += " WHERE estado = ?"
            count_query += " WHERE estado = ?"
            params.append(filtro_estado)
            count_params.append(filtro_estado)
        
        query += " ORDER BY nombre ASC LIMIT ? OFFSET ?"
        params.extend([por_pagina, offset])
        
        cursor.execute(query, tuple(params))
        resultados = cursor.fetchall()
        
        cursor.execute(count_query, tuple(count_params))
        total = cursor.fetchone()[0]
        conn.close()
        
        return {
            'datos': resultados,
            'total': total,
            'pagina_actual': pagina,
            'total_paginas': (total + por_pagina - 1) // por_pagina if total > 0 else 1,
            'por_pagina': por_pagina
        }
    
    @staticmethod
    def actualizar_estado(id_expediente, nuevo_estado):
        """Actualiza el estado de un expediente"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE expedientes SET estado = ?, fecha_actualizacion = ? WHERE id = ?",
            (nuevo_estado, datetime.now().strftime("%d/%m/%Y"), id_expediente)
        )
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def obtener_todos(filtro_estado="Todos"):
        """Obtiene todos los expedientes (usar para exportaciones)"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM expedientes"
        params = []
        
        if filtro_estado != "Todos":
            query += " WHERE estado = ?"
            params.append(filtro_estado)
        
        query += " ORDER BY nombre ASC"
        cursor.execute(query, tuple(params))
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    
    def nombre_completo(self):
        """Retorna el nombre completo del paciente"""
        partes = [self.nombre, self.apellido_paterno, self.apellido_materno]
        return " ".join([p for p in partes if p]).strip()