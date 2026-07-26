"""
Vista principal del sistema - SIN LICENCIA
"""
import customtkinter as ctk
from .registro_view import RegistroView
from .busqueda_view import BusquedaView
from .lista_view import ListaView
from .prestamo_view import PrestamoView
from .devolucion_view import DevolucionView
from .historial_view import HistorialView
from .reportes_view import ReportesView
from .ajustes_view import AjustesView
import sys
import os

class PrincipalView(ctk.CTkFrame):
    """Vista principal con pestañas"""
    
    def __init__(self, parent, usuario, rol):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent  # SistemaExpedientes
        self.usuario_actual = usuario
        self.rol_actual = rol
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz principal"""
        # Barra de título
        titulo_frame = ctk.CTkFrame(self, fg_color="#1F6AA5", height=60, corner_radius=0)
        titulo_frame.pack(fill="x", pady=(0, 10))
        titulo_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            titulo_frame,
            text="🏥 SISTEMA INTEGRAL PARA LA GESTIÓN DE EXPEDIENTES CLÍNICOS",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        ).pack(side="left", padx=20, pady=10)
        
        # Info usuario
        user_info = ctk.CTkFrame(titulo_frame, fg_color="transparent")
        user_info.pack(side="right", padx=20)
        
        ctk.CTkLabel(
            user_info,
            text=f"👤 {self.usuario_actual} ({self.rol_actual})",
            font=("Segoe UI", 12, "bold"),
            text_color="white"
        ).pack(side="left", padx=10)
        
        # ✅ ELIMINADO: ya no mostramos estado de licencia
        # Ya no hay SistemaLicencia
        
        ctk.CTkButton(
            user_info,
            text="🚪 Cerrar Sesión",
            command=self.cerrar_sesion,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=100,
            height=30
        ).pack(side="left", padx=10)
        
        # ✅ CREAR TABVIEW
        self.tabview = ctk.CTkTabview(
            self,
            width=1200,
            height=800,
            fg_color="white",
            corner_radius=20
        )
        self.tabview.pack(pady=15, padx=20, fill="both", expand=True)
        
        # Crear pestañas
        self.tab_lista = self.tabview.add("📋 LISTA")
        
        if self.rol_actual == "Consulta":
            # SOLO LECTURA
            self.tab_busqueda = self.tabview.add("🔍 BÚSQUEDA")
            self.tab_historial = self.tabview.add("📜 HISTORIAL")
            self.tab_reportes = self.tabview.add("📊 REPORTES")
            
            self.lista_view = ListaView(self.tab_lista, self, self.usuario_actual, self.rol_actual)
            self.busqueda_view = BusquedaView(self.tab_busqueda, self, self.usuario_actual, self.rol_actual)
            self.historial_view = HistorialView(self.tab_historial, self.usuario_actual)
            self.reportes_view = ReportesView(self.tab_reportes, self.usuario_actual)
            
            ctk.CTkLabel(
                self,
                text="🔒 Modo solo lectura - Solo puede ver información",
                font=("Segoe UI", 14, "bold"),
                text_color="#E74C3C"
            ).place(relx=0.02, rely=0.95, anchor="sw")
        else:
            # ADMIN y ARCHIVO
            self.tab_registro = self.tabview.add("📝 REGISTRO")
            self.tab_busqueda = self.tabview.add("🔍 BÚSQUEDA")
            self.tab_prestamo = self.tabview.add("📤 PRÉSTAMO")
            self.tab_devolucion = self.tabview.add("📥 DEVOLUCIÓN")
            self.tab_historial = self.tabview.add("📜 HISTORIAL")
            self.tab_reportes = self.tabview.add("📊 REPORTES")
            
            self.lista_view = ListaView(self.tab_lista, self, self.usuario_actual, self.rol_actual)
            self.registro_view = RegistroView(self.tab_registro, self, self.usuario_actual, self.rol_actual)
            self.busqueda_view = BusquedaView(self.tab_busqueda, self, self.usuario_actual, self.rol_actual)
            self.prestamo_view = PrestamoView(self.tab_prestamo, self, self.usuario_actual, self.rol_actual)
            self.devolucion_view = DevolucionView(self.tab_devolucion, self, self.usuario_actual, self.rol_actual)
            self.historial_view = HistorialView(self.tab_historial, self.usuario_actual)
            self.reportes_view = ReportesView(self.tab_reportes, self.usuario_actual)
        
        # Botón de ajustes (solo admin)
        if self.rol_actual == "Administrador":
            self.btn_ajustes = ctk.CTkButton(
                self,
                text="⚙️",
                width=45,
                height=45,
                corner_radius=22,
                fg_color="#0f3460",
                hover_color="#1a5276",
                font=("Segoe UI", 20),
                command=self.abrir_ajustes
            )
            self.btn_ajustes.place(relx=0.98, rely=0.98, anchor="se")
        
        # Barra de estado
        self.status_bar = ctk.CTkLabel(
            self,
            text="✅ Sistema listo",
            font=("Segoe UI", 11),
            text_color="gray",
            anchor="w"
        )
        self.status_bar.place(relx=0.02, rely=0.98, anchor="sw")
        
        # Atajos de teclado
        self.bind("<Control-l>", lambda e: self.tabview.set("📋 LISTA"))
        self.bind("<Control-g>", lambda e: self.registro_view.guardar() 
                  if hasattr(self, 'registro_view') and self.tabview.get() == "📝 REGISTRO" else None)
        self.bind("<Control-b>", lambda e: self.busqueda_view.focus_busqueda() 
                  if hasattr(self.busqueda_view, 'focus_busqueda') else None)
        self.bind("<Control-p>", lambda e: self.reportes_view.exportar_pdf())
        self.bind("<Control-x>", lambda e: self.reportes_view.exportar_excel())
        self.bind("<F1>", lambda e: self.mostrar_ayuda())
    
    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        import tkinter.messagebox as messagebox
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de cerrar sesión?"):
            self.parent.destroy()
            os.startfile(sys.argv[0])
    
    def abrir_ajustes(self):
        """Abre la ventana de configuración"""
        ajustes = AjustesView(self, self.usuario_actual)
        ajustes.mostrar()
    
    def mostrar_ayuda(self):
        """Muestra la ayuda del sistema"""
        import tkinter.messagebox as messagebox
        help_text = """
📖 SISTEMA DE EXPEDIENTES CLÍNICOS - AYUDA

👤 ROLES Y PERMISOS:
• Administrador: Acceso total + configuración
• Personal de Archivo: Registro, préstamo, devolución
• Consulta: 🔒 Solo lectura

⌨️ ATAJOS DE TECLADO:
Ctrl+L  → Ir a Lista de expedientes
Ctrl+G  → Guardar registro (Admin y Archivo)
Ctrl+B  → Enfocar buscador
Ctrl+P  → Exportar PDF
Ctrl+X  → Exportar Excel
F1      → Esta ayuda

📋 MÓDULOS:
1. LISTA: 📋 Ver todos los expedientes con CRUD
2. Registro: Crear nuevos expedientes (Admin y Archivo)
3. Búsqueda: Localizar expedientes por N°, nombre
4. Préstamo: Registrar préstamos (Admin y Archivo)
5. Devolución: Registrar devoluciones (Admin y Archivo)
6. Historial: Ver todo el historial del expediente
7. Reportes: Generar reportes y estadísticas

🔑 CRUD DISPONIBLE:
• Crear: ✅ Admin y Archivo
• Leer: ✅ Todos los roles
• Editar: ✅ Admin y Archivo
• Eliminar: ✅ Solo Admin
        """
        messagebox.showinfo("Ayuda - Sistema de Expedientes", help_text)