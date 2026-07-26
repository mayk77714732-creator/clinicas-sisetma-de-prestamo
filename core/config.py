"""
Configuración central del sistema - CORREGIDA PARA .EXE
"""
import os
import sys
from datetime import datetime

def obtener_ruta_base():
    """
    Obtiene la ruta base del sistema.
    - Si es .exe: usa la carpeta del ejecutable
    - Si es script: usa el escritorio
    """
    # Detectar si estamos ejecutando como .exe compilado
    if getattr(sys, 'frozen', False):
        # Ejecutando como .exe - usar carpeta del ejecutable
        base = os.path.dirname(sys.executable)
    else:
        # Ejecutando como script Python - usar escritorio
        escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(escritorio):
            escritorio = os.path.join(os.path.expanduser("~"), "Escritorio")
        base = escritorio
    
    return os.path.join(base, "SISTEMA_EXPEDIENTES")

# Rutas principales
BASE_DIR = obtener_ruta_base()
DB_PATH = os.path.join(BASE_DIR, "datos", "expedientes.db")
RESPALDOS_DIR = os.path.join(BASE_DIR, "respaldos")
REPORTES_DIR = os.path.join(BASE_DIR, "reportes")
EXCEL_DIR = os.path.join(REPORTES_DIR, "excel")
PDF_DIR = os.path.join(REPORTES_DIR, "pdf")

# Crear directorios necesarios
for dir_path in [BASE_DIR, os.path.dirname(DB_PATH), RESPALDOS_DIR, 
                 REPORTES_DIR, EXCEL_DIR, PDF_DIR]:
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except:
            pass  # Si falla, se intentará más tarde

# Configuración de la aplicación
APP_NAME = "Sistema Integral para la Gestión de Expedientes Clínicos"
APP_VERSION = "2.0"
APP_AUTHOR = "ProgreSoft"