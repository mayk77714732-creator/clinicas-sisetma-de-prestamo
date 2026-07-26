"""
Punto de entrada principal del sistema - SIN LICENCIA
"""
import customtkinter as ctk
from tkinter import messagebox
from core.database import Database
from views.login_view import LoginView
from views.principal_view import PrincipalView
import sys
import os
import traceback

class SistemaExpedientes(ctk.CTk):
    """Aplicación principal del sistema"""
    
    def __init__(self):
        super().__init__()
        
        try:
            self.title("Sistema Integral para la Gestión de Expedientes Clínicos")
            self.geometry("1400x900")
            self.configure(fg_color="#F0F4F8")
            self.resizable(True, True)
            self.minsize(1200, 768)
            
            # Intentar establecer tema
            try:
                ctk.set_appearance_mode("light")
                ctk.set_default_color_theme("blue")
            except:
                pass
            
            # Inicializar base de datos
            Database.initialize()
            
            # Mostrar login directamente (sin licencia)
            self.mostrar_login()
            
        except Exception as e:
            print(f"Error al iniciar: {traceback.format_exc()}")
            messagebox.showerror(
                "Error Crítico",
                f"Ocurrió un error al iniciar el sistema:\n\n{str(e)}\n\n"
                "Revise que tenga permisos de escritura en la carpeta del sistema."
            )
            self.destroy()
    
    def mostrar_login(self):
        """Muestra la ventana de login"""
        self.login = LoginView(self)
        self.login.pack(expand=True, fill="both")
    
    def iniciar_sistema(self, usuario, rol):
        """Inicia el sistema principal después del login"""
        try:
            self.login.destroy()
            self.principal = PrincipalView(self, usuario, rol)
            self.principal.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error al iniciar sistema: {e}")
            messagebox.showerror("Error", f"No se pudo iniciar el sistema: {str(e)}")

if __name__ == "__main__":
    try:
        app = SistemaExpedientes()
        app.mainloop()
    except Exception as e:
        print(f"Error fatal: {traceback.format_exc()}")
        input("Presione Enter para salir...")