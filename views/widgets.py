"""
Widgets personalizados para la interfaz
"""
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
import os  # <--- AGREGAR ESTA LÍNEA

class DateEntry(ctk.CTkFrame):
    """Campo de fecha con botón para calendario"""
    
    def __init__(self, master, placeholder_text="DD/MM/AAAA", width=250, height=40, **kwargs):
        super().__init__(master, fg_color="transparent")
        
        self.width = width
        self.height = height
        
        self.entry = ctk.CTkEntry(
            self, 
            placeholder_text=placeholder_text,
            width=width - 50,
            height=height,
            **kwargs
        )
        self.entry.pack(side="left", padx=(0, 5))
        
        self.btn_calendario = ctk.CTkButton(
            self,
            text="📅",
            width=40,
            height=height,
            command=self.abrir_calendario,
            fg_color="#3498DB",
            hover_color="#2980B9"
        )
        self.btn_calendario.pack(side="left")
        
        self.fecha_seleccionada = None
    
    def abrir_calendario(self):
        """Abre un calendario para seleccionar fecha"""
        try:
            from tkcalendar import Calendar
            
            ventana = ctk.CTkToplevel(self)
            ventana.title("Seleccionar fecha")
            ventana.geometry("320x320")
            ventana.configure(fg_color="#F8F9FA")
            ventana.grab_set()
            ventana.resizable(False, False)
            
            cal = Calendar(
                ventana,
                selectmode='day',
                date_pattern='dd/mm/yyyy',
                year=datetime.now().year,
                month=datetime.now().month,
                day=datetime.now().day
            )
            cal.pack(pady=20, padx=20)
            
            btn_frame = ctk.CTkFrame(ventana, fg_color="transparent")
            btn_frame.pack(pady=10)
            
            def seleccionar():
                self.entry.delete(0, 'end')
                self.entry.insert(0, cal.get_date())
                self.fecha_seleccionada = cal.get_date()
                ventana.destroy()
            
            ctk.CTkButton(
                btn_frame,
                text="✅ Seleccionar",
                command=seleccionar,
                fg_color="#4CAF50",
                hover_color="#388E3C",
                width=100
            ).pack(side="left", padx=5)
            
            ctk.CTkButton(
                btn_frame,
                text="❌ Cancelar",
                command=ventana.destroy,
                fg_color="#E74C3C",
                hover_color="#C0392B",
                width=100
            ).pack(side="left", padx=5)
            
        except ImportError:
            messagebox.showwarning(
                "Calendario no disponible",
                "Instale tkcalendar para usar el calendario:\n\npip install tkcalendar"
            )
    
    def get(self):
        return self.entry.get()
    
    def delete(self, first, last=None):
        self.entry.delete(first, last)
    
    def insert(self, index, string):
        self.entry.insert(index, string)
    
    def configure(self, **kwargs):
        self.entry.configure(**kwargs)
    
    def set_date(self, fecha):
        self.entry.delete(0, 'end')
        self.entry.insert(0, fecha)
        self.fecha_seleccionada = fecha