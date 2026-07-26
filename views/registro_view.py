"""
Vista de registro de expedientes - SIN CURP Y CON MEJOR ALINEACIÓN
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from .widgets import DateEntry
from models.expediente import Expediente
from models.historial import Historial
from core.database import Database

class RegistroView:
    """Vista para registrar nuevos expedientes"""
    
    def __init__(self, parent, principal, usuario_actual, rol_actual):
        self.parent = parent
        self.principal = principal
        self.usuario_actual = usuario_actual
        self.rol_actual = rol_actual
        self.frame = None
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de registro con mejor alineación"""
        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Título
        ctk.CTkLabel(
            self.frame,
            text="📝 REGISTRO DE EXPEDIENTE",
            font=("Segoe UI", 26, "bold"),
            text_color="#1F6AA5"
        ).pack(pady=(10, 25))
        
        # --- FORMULARIO MEJORADO ---
        form_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        form_frame.pack(pady=5)
        
        # ========== FILA 1: Nombre ==========
        ctk.CTkLabel(form_frame, text="Nombre:", font=("Segoe UI", 13, "bold"), 
                    text_color="#2C3E50").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 2))
        
        # Sub-fila para nombre completo (3 campos en una fila)
        nombre_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        nombre_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        
        self.nombre = ctk.CTkEntry(
            nombre_frame, 
            placeholder_text="Nombre", 
            width=180, 
            height=40,
            font=("Segoe UI", 13)
        )
        self.nombre.pack(side="left", padx=(0, 10))
        
        self.apellido_p = ctk.CTkEntry(
            nombre_frame, 
            placeholder_text="Apellido Paterno", 
            width=200, 
            height=40,
            font=("Segoe UI", 13)
        )
        self.apellido_p.pack(side="left", padx=(0, 10))
        
        self.apellido_m = ctk.CTkEntry(
            nombre_frame, 
            placeholder_text="Apellido Materno", 
            width=200, 
            height=40,
            font=("Segoe UI", 13)
        )
        self.apellido_m.pack(side="left")
        
        # ========== FILA 2: Fecha Nacimiento y Sexo ==========
        ctk.CTkLabel(form_frame, text="Fecha de Nacimiento:", font=("Segoe UI", 13, "bold"), 
                    text_color="#2C3E50").grid(row=2, column=0, sticky="w", padx=10, pady=(10, 2))
        
        self.fecha_nac = DateEntry(
            form_frame, 
            placeholder_text="DD/MM/AAAA", 
            width=220, 
            height=40
        )
        self.fecha_nac.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")
        
        ctk.CTkLabel(form_frame, text="Sexo:", font=("Segoe UI", 13, "bold"), 
                    text_color="#2C3E50").grid(row=2, column=1, sticky="w", padx=10, pady=(10, 2))
        
        self.sexo = ctk.CTkComboBox(
            form_frame, 
            values=["Masculino", "Femenino"], 
            width=200, 
            height=40,
            font=("Segoe UI", 13)
        )
        self.sexo.grid(row=3, column=1, padx=10, pady=(0, 10), sticky="w")
        self.sexo.set("Masculino")
        
        # ========== FILA 3: Colonia ==========
        ctk.CTkLabel(form_frame, text="Colonia:", font=("Segoe UI", 13, "bold"), 
                    text_color="#2C3E50").grid(row=4, column=0, sticky="w", padx=10, pady=(10, 2))
        
        self.colonia = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Colonia donde reside", 
            width=450, 
            height=40,
            font=("Segoe UI", 13)
        )
        self.colonia.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")
        
        # ========== FILA 4: Estado ==========
        ctk.CTkLabel(form_frame, text="Estado Inicial:", font=("Segoe UI", 13, "bold"), 
                    text_color="#2C3E50").grid(row=6, column=0, sticky="w", padx=10, pady=(10, 2))
        
        self.estado = ctk.CTkComboBox(
            form_frame, 
            values=["Disponible", "Prestado", "Archivo muerto"], 
            width=200, 
            height=40,
            font=("Segoe UI", 13)
        )
        self.estado.grid(row=7, column=0, padx=10, pady=(0, 10), sticky="w")
        self.estado.set("Disponible")
        
        # ========== BOTÓN GUARDAR ==========
        btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        estado_boton = "disabled" if self.rol_actual == "Consulta" else "normal"
        
        self.btn_guardar = ctk.CTkButton(
            btn_frame,
            text="💾 GUARDAR EXPEDIENTE (Ctrl+G)",
            command=self.guardar,
            fg_color="#4CAF50" if self.rol_actual != "Consulta" else "#95A5A6",
            hover_color="#388E3C" if self.rol_actual != "Consulta" else "#95A5A6",
            width=400,
            height=55,
            font=("Segoe UI", 17, "bold"),
            state=estado_boton,
            corner_radius=12
        )
        self.btn_guardar.pack()
        
        # Mensaje para modo consulta
        if self.rol_actual == "Consulta":
            ctk.CTkLabel(
                self.frame,
                text="🔒 Modo solo lectura - No puede registrar expedientes",
                font=("Segoe UI", 13, "bold"),
                text_color="#E74C3C"
            ).pack(pady=10)
        
        # Atajo de teclado
        self.frame.bind("<Control-g>", lambda e: self.guardar())
        self.frame.focus_set()
        
        # Enfocar primer campo
        self.nombre.focus()
    
    def guardar(self):
        """Guarda el expediente en la base de datos - SIN CURP"""
        if self.rol_actual == "Consulta":
            messagebox.showwarning("Acceso denegado", "El rol Consulta solo tiene permisos de lectura.")
            return
        
        try:
            # Obtener datos del formulario
            nombre = self.nombre.get().strip().title()
            apellido_p = self.apellido_p.get().strip().title()
            apellido_m = self.apellido_m.get().strip().title()
            fecha_nac = self.fecha_nac.get().strip()
            sexo = self.sexo.get()
            colonia = self.colonia.get().strip()
            estado = self.estado.get()
            
            # Validar campos obligatorios
            if not nombre or not apellido_p:
                messagebox.showwarning("Incompleto", "Complete Nombre y Apellido Paterno.")
                self.nombre.focus()
                return
            
            # Validar fecha
            try:
                datetime.strptime(fecha_nac, "%d/%m/%Y")
            except:
                messagebox.showwarning("Fecha inválida", "La fecha debe tener formato DD/MM/AAAA")
                self.fecha_nac.focus()
                return
            
            # Crear expediente
            expediente = Expediente(
                nombre=nombre,
                apellido_p=apellido_p,
                apellido_m=apellido_m,
                fecha_nac=fecha_nac,
                sexo=sexo,
                colonia=colonia,
                estado=estado
            )
            
            # Guardar
            id_exp = expediente.guardar()
            
            if id_exp:
                # Registrar historial
                Historial.registrar(
                    id_exp,
                    "Registro",
                    f"Expediente registrado: {expediente.nombre_completo()}",
                    self.usuario_actual
                )
                
                # Limpiar formulario
                self.limpiar_formulario()
                
                messagebox.showinfo(
                    "Éxito",
                    f"✅ Expediente #{expediente.numero} registrado correctamente."
                )
                
                # Actualizar siguiente número
                self.actualizar_siguiente_numero()
                
                # Refrescar listas
                if hasattr(self.principal, 'busqueda_view'):
                    self.principal.busqueda_view.refrescar()
                if hasattr(self.principal, 'lista_view'):
                    self.principal.lista_view.cargar_datos()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.nombre.delete(0, 'end')
        self.apellido_p.delete(0, 'end')
        self.apellido_m.delete(0, 'end')
        self.fecha_nac.delete(0, 'end')
        self.colonia.delete(0, 'end')
        self.sexo.set("Masculino")
        self.estado.set("Disponible")
        self.nombre.focus()
    
    def actualizar_siguiente_numero(self):
        """Muestra el siguiente número de expediente disponible"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(numero_expediente) FROM expedientes")
        max_num = cursor.fetchone()[0] or 0
        conn.close()
        if hasattr(self.principal, 'status_bar'):
            self.principal.status_bar.configure(
                text=f"✅ Siguiente número: {max_num + 1}",
                text_color="green"
            )