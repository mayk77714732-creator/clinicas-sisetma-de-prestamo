"""
Vista de préstamo de expedientes - CORREGIDA COMPLETA
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from .widgets import DateEntry
from models.expediente import Expediente
from models.prestamo import Prestamo
from models.historial import Historial

class PrestamoView:
    """Vista para registrar préstamos"""
    
    def __init__(self, parent, principal, usuario_actual, rol_actual):
        self.parent = parent
        self.principal = principal
        self.usuario_actual = usuario_actual
        self.rol_actual = rol_actual
        self.frame = None
        self.expediente_actual = None
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de préstamo"""
        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            self.frame,
            text="📤 REGISTRO DE PRÉSTAMO",
            font=("Segoe UI", 24, "bold"),
            text_color="#1F6AA5"
        ).pack(pady=(10, 20))
        
        # Buscar expediente
        search_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        search_frame.pack(pady=10)
        
        ctk.CTkLabel(search_frame, text="Número de expediente:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=10)
        self.buscar_input = ctk.CTkEntry(search_frame, placeholder_text="Número", width=150, height=40)
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
        
        # Información del expediente
        self.info_frame = ctk.CTkFrame(self.frame, fg_color="white", corner_radius=12)
        self.info_frame.pack(fill="x", pady=10, padx=20)
        
        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text="🔍 Busque un expediente para comenzar",
            font=("Segoe UI", 14),
            text_color="gray"
        )
        self.info_label.pack(pady=20)
        
        # Formulario de préstamo
        self.form_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.form_frame.pack(pady=10)
        
        ctk.CTkLabel(self.form_frame, text="Solicitado por:", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, sticky="w", padx=10
        )
        self.solicitante = ctk.CTkEntry(self.form_frame, placeholder_text="Dr. Nombre", width=250, height=40)
        self.solicitante.grid(row=1, column=0, padx=10, pady=5)
        
        ctk.CTkLabel(self.form_frame, text="Área:", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=1, sticky="w", padx=10
        )
        self.area = ctk.CTkComboBox(
            self.form_frame,
            values=["Consulta Externa", "Urgencias", "Medicina General", "Pediatría", "Ginecología"],
            width=250,
            height=40
        )
        self.area.grid(row=1, column=1, padx=10, pady=5)
        self.area.set("Consulta Externa")
        
        ctk.CTkLabel(self.form_frame, text="Motivo:", font=("Segoe UI", 12, "bold")).grid(
            row=2, column=0, sticky="w", padx=10
        )
        self.motivo = ctk.CTkEntry(self.form_frame, placeholder_text="Motivo del préstamo", width=520, height=40)
        self.motivo.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        
        ctk.CTkLabel(self.form_frame, text="Fecha préstamo:", font=("Segoe UI", 12, "bold")).grid(
            row=4, column=0, sticky="w", padx=10
        )
        self.fecha_prestamo = DateEntry(self.form_frame, placeholder_text="DD/MM/AAAA", width=250, height=40)
        self.fecha_prestamo.grid(row=5, column=0, padx=10, pady=5)
        self.fecha_prestamo.set_date(datetime.now().strftime("%d/%m/%Y"))
        
        ctk.CTkLabel(self.form_frame, text="Fecha devolución:", font=("Segoe UI", 12, "bold")).grid(
            row=4, column=1, sticky="w", padx=10
        )
        self.fecha_devolucion = DateEntry(self.form_frame, placeholder_text="DD/MM/AAAA", width=250, height=40)
        self.fecha_devolucion.grid(row=5, column=1, padx=10, pady=5)
        self.fecha_devolucion.set_date((datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y"))
        
        btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        self.btn_registrar = ctk.CTkButton(
            btn_frame,
            text="✅ REGISTRAR PRÉSTAMO",
            command=self.registrar_prestamo,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=350,
            height=50,
            font=("Segoe UI", 16, "bold"),
            state="disabled"
        )
        self.btn_registrar.pack()
        
        self.habilitar_formulario(False)
    
    def habilitar_formulario(self, habilitado):
        estado = "normal" if habilitado else "disabled"
        self.solicitante.configure(state=estado)
        self.area.configure(state=estado)
        self.motivo.configure(state=estado)
        self.fecha_prestamo.configure(state=estado)
        self.fecha_devolucion.configure(state=estado)
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
        
        if resultado[8] != "Disponible":
            messagebox.showwarning(
                "No disponible",
                f"El expediente {numero} no está disponible.\nEstado actual: {resultado[8]}"
            )
            return
        
        nombre_completo = f"{resultado[2]} {resultado[3]} {resultado[4]}".strip()
        self.info_label.configure(
            text=f"✅ Expediente: {numero}  |  Paciente: {nombre_completo}  |  Estado: {resultado[8]}",
            text_color="green"
        )
        
        self.expediente_actual = resultado
        self.habilitar_formulario(True)
    
    def registrar_prestamo(self):
        if self.rol_actual == "Consulta":
            messagebox.showwarning("Acceso denegado", "El rol Consulta no puede registrar préstamos.")
            return
        
        if not self.expediente_actual:
            messagebox.showwarning("Error", "Primero busque un expediente disponible.")
            return
        
        solicitante = self.solicitante.get().strip()
        area = self.area.get()
        motivo = self.motivo.get().strip()
        fecha_prestamo = self.fecha_prestamo.get().strip()
        fecha_limite = self.fecha_devolucion.get().strip()
        
        if not solicitante or not motivo:
            messagebox.showwarning("Incompleto", "Complete todos los campos del préstamo.")
            return
        
        try:
            fecha_p = datetime.strptime(fecha_prestamo, "%d/%m/%Y")
            fecha_l = datetime.strptime(fecha_limite, "%d/%m/%Y")
            if fecha_l < fecha_p:
                messagebox.showwarning("Fecha inválida", "La fecha de devolución debe ser posterior.")
                return
        except:
            messagebox.showwarning("Fecha inválida", "Las fechas deben tener formato DD/MM/AAAA")
            return
        
        prestamo = Prestamo(
            id_expediente=self.expediente_actual[0],
            solicitado_por=solicitante,
            area=area,
            motivo=motivo,
            fecha_prestamo=fecha_prestamo,
            fecha_limite=fecha_limite
        )
        
        if prestamo.guardar():
            Expediente.actualizar_estado(self.expediente_actual[0], "Prestado")
            
            nombre_completo = f"{self.expediente_actual[2]} {self.expediente_actual[3]} {self.expediente_actual[4]}".strip()
            Historial.registrar(
                self.expediente_actual[0],
                "Préstamo",
                f"Expediente prestado a {area} por {solicitante}. Motivo: {motivo}",
                self.usuario_actual
            )
            
            self.buscar_input.delete(0, 'end')
            self.solicitante.delete(0, 'end')
            self.motivo.delete(0, 'end')
            self.info_label.configure(text="🔍 Busque un expediente para comenzar", text_color="gray")
            self.habilitar_formulario(False)
            self.expediente_actual = None
            
            messagebox.showinfo("Éxito", "Préstamo registrado correctamente.")