"""
Vista de historial de expedientes - CORREGIDA COMPLETA
"""
import customtkinter as ctk
from tkinter import messagebox
from models.historial import Historial
from models.expediente import Expediente

class HistorialView:
    """Vista para ver el historial de expedientes"""
    
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.frame = None
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de historial"""
        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            self.frame,
            text="📜 HISTORIAL DE EXPEDIENTES",
            font=("Segoe UI", 24, "bold"),
            text_color="#1F6AA5"
        ).pack(pady=(10, 15))
        
        search_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        search_frame.pack(pady=10)
        
        ctk.CTkLabel(search_frame, text="Seleccionar expediente:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=10)
        self.buscar_input = ctk.CTkEntry(search_frame, placeholder_text="N° Expediente", width=150, height=40)
        self.buscar_input.pack(side="left", padx=10)
        
        ctk.CTkButton(
            search_frame,
            text="🔍 Ver Historial",
            command=self.ver_historial,
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            width=150,
            height=40
        ).pack(side="left", padx=10)
        
        self.historial_frame = ctk.CTkFrame(self.frame, fg_color="white", corner_radius=12)
        self.historial_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        self.historial_label = ctk.CTkLabel(
            self.historial_frame,
            text="🔍 Busque un expediente para ver su historial",
            font=("Segoe UI", 16),
            text_color="gray"
        )
        self.historial_label.pack(pady=50)
    
    def cargar_expediente(self, numero):
        self.buscar_input.delete(0, 'end')
        self.buscar_input.insert(0, str(numero))
        self.ver_historial()
    
    def ver_historial(self):
        try:
            numero = int(self.buscar_input.get().strip())
        except:
            messagebox.showwarning("Incompleto", "Ingrese un número de expediente válido.")
            return
        
        exp = Expediente.obtener_por_numero(numero)
        
        if not exp:
            messagebox.showerror("No encontrado", f"No se encontró el expediente {numero}")
            return
        
        historial = Historial.obtener_por_expediente(exp[0])
        self._mostrar_historial(historial, exp)
    
    def _mostrar_historial(self, historial, exp):
        for widget in self.historial_frame.winfo_children():
            widget.destroy()
        
        nombre_completo = f"{exp[2]} {exp[3]} {exp[4]}".strip()
        
        ctk.CTkLabel(
            self.historial_frame,
            text=f"📜 HISTORIAL - {nombre_completo}",
            font=("Segoe UI", 18, "bold"),
            text_color="#1F6AA5"
        ).pack(pady=10)
        
        ctk.CTkLabel(
            self.historial_frame,
            text=f"Expediente: {exp[1]}  |  Estado: {exp[8]}",
            font=("Segoe UI", 12),
            text_color="#555"
        ).pack(pady=5)
        
        if not historial:
            ctk.CTkLabel(
                self.historial_frame,
                text="❌ No hay registros en el historial",
                font=("Segoe UI", 14),
                text_color="gray"
            ).pack(pady=50)
            return
        
        scroll_frame = ctk.CTkScrollableFrame(
            self.historial_frame,
            fg_color="white",
            corner_radius=10
        )
        scroll_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        headers = ["Fecha", "Acción", "Descripción"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                scroll_frame,
                text=header,
                font=("Segoe UI", 12, "bold"),
                text_color="#2C3E50",
                width=150
            ).grid(row=0, column=i, padx=10, pady=10, sticky="w")
        
        for i, reg in enumerate(historial):
            row = i + 1
            ctk.CTkLabel(
                scroll_frame,
                text=reg[3],
                font=("Segoe UI", 11),
                text_color="#333",
                width=150
            ).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            colores = {"Registro": "#27AE60", "Préstamo": "#F39C12", "Devolución": "#3498DB"}
            color = colores.get(reg[2], "#7F8C8D")
            
            ctk.CTkLabel(
                scroll_frame,
                text=reg[2],
                font=("Segoe UI", 11, "bold"),
                text_color=color,
                width=150
            ).grid(row=row, column=1, padx=10, pady=5, sticky="w")
            
            ctk.CTkLabel(
                scroll_frame,
                text=reg[4],
                font=("Segoe UI", 11),
                text_color="#555",
                width=150
            ).grid(row=row, column=2, padx=10, pady=5, sticky="w")