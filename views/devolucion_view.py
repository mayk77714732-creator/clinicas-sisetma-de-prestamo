"""
Vista de devolución de expedientes - CORREGIDA COMPLETA
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from .widgets import DateEntry
from models.expediente import Expediente
from models.prestamo import Prestamo
from models.historial import Historial

class DevolucionView:
    """Vista para registrar devoluciones"""
    
    def __init__(self, parent, principal, usuario_actual, rol_actual):
        self.parent = parent
        self.principal = principal
        self.usuario_actual = usuario_actual
        self.rol_actual = rol_actual
        self.frame = None
        self.expediente_actual = None
        self.prestamo_actual = None
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de devolución"""
        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            self.frame,
            text="📥 REGISTRO DE DEVOLUCIÓN",
            font=("Segoe UI", 24, "bold"),
            text_color="#1F6AA5"
        ).pack(pady=(10, 20))
        
        search_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        search_frame.pack(pady=10)
        
        ctk.CTkLabel(search_frame, text="Buscar expediente:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=10)
        self.buscar_input = ctk.CTkEntry(search_frame, placeholder_text="N° Expediente", width=150, height=40)
        self.buscar_input.pack(side="left", padx=10)
        
        ctk.CTkButton(
            search_frame,
            text="🔍 Buscar",
            command=self.buscar_expediente,
            fg_color="#3498DB",
            hover_color="#2980B9",
            width=100,
            height=40
        ).pack(side="left", padx=10)
        
        self.info_frame = ctk.CTkFrame(self.frame, fg_color="white", corner_radius=12)
        self.info_frame.pack(fill="x", pady=10, padx=20)
        
        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text="🔍 Busque un expediente prestado para devolver",
            font=("Segoe UI", 14),
            text_color="gray"
        )
        self.info_label.pack(pady=20)
        
        self.form_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.form_frame.pack(pady=10)
        
        ctk.CTkLabel(self.form_frame, text="Devuelto por:", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, sticky="w", padx=10
        )
        self.devuelto_por = ctk.CTkEntry(self.form_frame, placeholder_text="Nombre de quien devuelve", width=250, height=40)
        self.devuelto_por.grid(row=1, column=0, padx=10, pady=5)
        
        ctk.CTkLabel(self.form_frame, text="Fecha devolución:", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=1, sticky="w", padx=10
        )
        self.fecha_devolucion = DateEntry(self.form_frame, placeholder_text="DD/MM/AAAA", width=250, height=40)
        self.fecha_devolucion.grid(row=1, column=1, padx=10, pady=5)
        self.fecha_devolucion.set_date(datetime.now().strftime("%d/%m/%Y"))
        
        ctk.CTkLabel(self.form_frame, text="Observaciones:", font=("Segoe UI", 12, "bold")).grid(
            row=2, column=0, sticky="w", padx=10
        )
        self.observaciones = ctk.CTkEntry(self.form_frame, placeholder_text="Observaciones adicionales", width=520, height=40)
        self.observaciones.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        
        btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        self.btn_registrar = ctk.CTkButton(
            btn_frame,
            text="✅ REGISTRAR DEVOLUCIÓN",
            command=self.registrar_devolucion,
            fg_color="#27AE60",
            hover_color="#219150",
            width=350,
            height=50,
            font=("Segoe UI", 16, "bold"),
            state="disabled"
        )
        self.btn_registrar.pack()
        
        self.habilitar_formulario(False)
    
    def habilitar_formulario(self, habilitado):
        estado = "normal" if habilitado else "disabled"
        self.devuelto_por.configure(state=estado)
        self.fecha_devolucion.configure(state=estado)
        self.observaciones.configure(state=estado)
        self.btn_registrar.configure(state="normal" if habilitado else "disabled")
    
    def cargar_expediente(self, numero):
        self.buscar_input.delete(0, 'end')
        self.buscar_input.insert(0, str(numero))
        self.buscar_expediente()
    
    def buscar_expediente(self):
        try:
            numero = int(self.buscar_input.get().strip())
        except:
            messagebox.showwarning("Incompleto", "Ingrese un número de expediente válido.")
            return
        
        resultado = Expediente.obtener_por_numero(numero)
        
        if not resultado:
            messagebox.showerror("No encontrado", f"No se encontró el expediente {numero}")
            return
        
        if resultado[8] != "Prestado":
            messagebox.showwarning(
                "No prestado",
                f"El expediente {numero} no está prestado.\nEstado actual: {resultado[8]}"
            )
            return
        
        prestamo = Prestamo.obtener_activo_por_expediente(resultado[0])
        
        if not prestamo:
            messagebox.showerror("Error", "El expediente está marcado como prestado pero no hay registro.")
            return
        
        nombre_completo = f"{resultado[2]} {resultado[3]} {resultado[4]}".strip()
        info_text = f"✅ Expediente: {numero}  |  Paciente: {nombre_completo}\n"
        info_text += f"📤 Prestado a: {prestamo[3]}  |  Solicitado por: {prestamo[2]}\n"
        info_text += f"📅 Fecha préstamo: {prestamo[5]}  |  Límite: {prestamo[6]}"
        
        self.info_label.configure(text=info_text, text_color="green")
        self.expediente_actual = resultado
        self.prestamo_actual = prestamo
        self.habilitar_formulario(True)
    
    def registrar_devolucion(self):
        if self.rol_actual == "Consulta":
            messagebox.showwarning("Acceso denegado", "El rol Consulta no puede registrar devoluciones.")
            return
        
        if not self.expediente_actual or not self.prestamo_actual:
            messagebox.showwarning("Error", "Primero busque un expediente prestado.")
            return
        
        devuelto_por = self.devuelto_por.get().strip()
        fecha_dev = self.fecha_devolucion.get().strip()
        obs = self.observaciones.get().strip()
        
        if not devuelto_por:
            messagebox.showwarning("Incompleto", "Ingrese quién devuelve el expediente.")
            return
        
        try:
            datetime.strptime(fecha_dev, "%d/%m/%Y")
        except:
            messagebox.showwarning("Fecha inválida", "La fecha debe tener formato DD/MM/AAAA")
            return
        
        Prestamo.registrar_devolucion(self.prestamo_actual[0], fecha_dev, devuelto_por)
        Expediente.actualizar_estado(self.expediente_actual[0], "Disponible")
        
        nombre_completo = f"{self.expediente_actual[2]} {self.expediente_actual[3]} {self.expediente_actual[4]}".strip()
        Historial.registrar(
            self.expediente_actual[0],
            "Devolución",
            f"Expediente devuelto por {devuelto_por}. Observaciones: {obs if obs else 'Ninguna'}",
            self.usuario_actual
        )
        
        self.buscar_input.delete(0, 'end')
        self.devuelto_por.delete(0, 'end')
        self.observaciones.delete(0, 'end')
        self.info_label.configure(text="🔍 Busque un expediente prestado para devolver", text_color="gray")
        self.habilitar_formulario(False)
        self.expediente_actual = None
        self.prestamo_actual = None
        
        messagebox.showinfo("Éxito", "Devolución registrada correctamente.")