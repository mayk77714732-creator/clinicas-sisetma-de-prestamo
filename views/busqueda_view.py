"""
Vista de búsqueda de expedientes - CON VENTANA DE DETALLES MEJORADA
"""
import customtkinter as ctk
from tkinter import messagebox
from models.expediente import Expediente
from models.prestamo import Prestamo

class BusquedaView:
    """Vista para buscar expedientes"""
    
    def __init__(self, parent, principal, usuario_actual, rol_actual):
        self.parent = parent
        self.principal = principal
        self.usuario_actual = usuario_actual
        self.rol_actual = rol_actual
        self.frame = None
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de búsqueda"""
        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            self.frame,
            text="🔍 BÚSQUEDA RÁPIDA DE EXPEDIENTES (Ctrl+B)",
            font=("Segoe UI", 24, "bold"),
            text_color="#1F6AA5"
        ).pack(pady=(10, 15))
        
        search_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        search_frame.pack(pady=10)
        
        self.bus_input = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar por N° Expediente o Nombre...",
            width=450,
            height=45,
            font=("Segoe UI", 14)
        )
        self.bus_input.grid(row=0, column=0, padx=10)
        self.bus_input.bind("<Return>", lambda e: self.buscar())
        
        self.bus_tipo = ctk.CTkComboBox(
            search_frame,
            values=["Todos", "Disponible", "Prestado", "Archivo muerto"],
            width=120,
            height=40
        )
        self.bus_tipo.grid(row=0, column=1, padx=5)
        self.bus_tipo.set("Todos")
        
        ctk.CTkButton(
            search_frame,
            text="🔍 BUSCAR",
            command=self.buscar,
            fg_color="#FF9800",
            hover_color="#F57C00",
            height=45,
            width=120,
            font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=2, padx=10)
        
        self.scroll_resultados = ctk.CTkScrollableFrame(
            self.frame,
            width=900,
            height=450,
            fg_color="white",
            border_width=1,
            border_color="#BDC3C7",
            corner_radius=10
        )
        self.scroll_resultados.pack(pady=15, padx=10, fill="both", expand=True)
    
    def focus_busqueda(self):
        self.bus_input.focus()
    
    def buscar(self):
        """Realiza la búsqueda de expedientes con límite de 100 resultados"""
        termino = self.bus_input.get().strip()
        filtro_estado = self.bus_tipo.get()
        
        for widget in self.scroll_resultados.winfo_children():
            widget.destroy()
        
        if not termino:
            ctk.CTkLabel(
                self.scroll_resultados,
                text="✏️ Ingrese un término de búsqueda.",
                font=("Segoe UI", 16),
                text_color="gray"
            ).pack(pady=50)
            return
        
        resultados = Expediente.buscar(termino, filtro_estado, limite=100)
        
        if not resultados:
            ctk.CTkLabel(
                self.scroll_resultados,
                text=f"❌ No se encontraron expedientes con: '{termino}'",
                font=("Segoe UI", 16),
                text_color="#E74C3C"
            ).pack(pady=50)
            return
        
        if len(resultados) == 100:
            ctk.CTkLabel(
                self.scroll_resultados,
                text=f"⚠️ Mostrando primeros 100 resultados. Refine su búsqueda.",
                font=("Segoe UI", 12),
                text_color="#F39C12"
            ).pack(pady=5)
        
        for fila in resultados:
            self._crear_tarjeta(fila)
        
        if hasattr(self.principal, 'status_bar'):
            self.principal.status_bar.configure(
                text=f"🔍 {len(resultados)} resultados encontrados",
                text_color="blue"
            )
    
    def _crear_tarjeta(self, fila):
        """Crea una tarjeta de resultado"""
        tarjeta = ctk.CTkFrame(
            self.scroll_resultados,
            fg_color="white",
            border_width=1,
            border_color="#3498DB",
            corner_radius=12
        )
        tarjeta.pack(fill="x", pady=8, padx=10, ipadx=10, ipady=8)
        
        info_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        info_frame.pack(fill="x", pady=5)
        
        nombre_completo = f"{fila[2]} {fila[3]} {fila[4]}".strip()
        
        ctk.CTkLabel(
            info_frame,
            text=f"📋 #{fila[1]} - {nombre_completo}",
            font=("Segoe UI", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w")
        
        info_text = f"Colonia: {fila[7] if fila[7] else '—'}"
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=("Segoe UI", 12),
            text_color="#555"
        ).pack(anchor="w")
        
        estado = fila[8]
        colores = {"Disponible": "#27AE60", "Prestado": "#F39C12", "Archivo muerto": "#95A5A6"}
        color = colores.get(estado, "#7F8C8D")
        
        ctk.CTkLabel(
            info_frame,
            text=f"Estado: {estado}",
            font=("Segoe UI", 12, "bold"),
            text_color=color
        ).pack(anchor="w")
        
        if estado == "Prestado":
            prestamo = Prestamo.obtener_activo_por_expediente(fila[0])
            if prestamo:
                ctk.CTkLabel(
                    info_frame,
                    text=f"📤 Prestado a: {prestamo[3]}  |  Solicitado por: {prestamo[2]}",
                    font=("Segoe UI", 11),
                    text_color="#856404"
                ).pack(anchor="w")
                ctk.CTkLabel(
                    info_frame,
                    text=f"📅 Fecha límite: {prestamo[6]}",
                    font=("Segoe UI", 11),
                    text_color="#856404"
                ).pack(anchor="w")
        
        btn_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        btn_frame.pack(fill="x", pady=5)
        
        ctk.CTkButton(
            btn_frame,
            text="👁️ Ver",
            width=80,
            fg_color="#3498DB",
            hover_color="#2980B9",
            command=lambda f=fila: self._ver_detalles(f)
        ).pack(side="left", padx=3)
        
        if self.rol_actual != "Consulta":
            if estado == "Disponible":
                ctk.CTkButton(
                    btn_frame,
                    text="📤 Prestar",
                    width=80,
                    fg_color="#F39C12",
                    hover_color="#D68910",
                    command=lambda f=fila: self._prestar(f)
                ).pack(side="left", padx=3)
            elif estado == "Prestado":
                ctk.CTkButton(
                    btn_frame,
                    text="📥 Devolver",
                    width=80,
                    fg_color="#27AE60",
                    hover_color="#219150",
                    command=lambda f=fila: self._devolver(f)
                ).pack(side="left", padx=3)
        
        ctk.CTkButton(
            btn_frame,
            text="📜 Historial",
            width=80,
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            command=lambda f=fila: self._ver_historial(f)
        ).pack(side="left", padx=3)
    
    # ==========================================
    # ✅ VENTANA DE DETALLES MEJORADA
    # ==========================================
    def _ver_detalles(self, fila):
        """Muestra detalles del expediente en una ventana profesional"""
        
        # Crear ventana
        ventana = ctk.CTkToplevel(self.principal)
        ventana.title(f"Detalles del Expediente #{fila[1]}")
        ventana.geometry("650x550")
        ventana.configure(fg_color="#F8F9FA")
        ventana.resizable(False, False)
        ventana.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(ventana, fg_color="white", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ===== CABECERA CON NOMBRE =====
        nombre_completo = f"{fila[2]} {fila[3]} {fila[4]}".strip()
        
        header_frame = ctk.CTkFrame(main_frame, fg_color="#1F6AA5", corner_radius=10)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(
            header_frame,
            text=f"👤 {nombre_completo}",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        ).pack(pady=15, padx=20)
        
        # ===== INFORMACIÓN DEL EXPEDIENTE =====
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        # Estado con color
        estado = fila[8]
        colores_estado = {
            "Disponible": "#27AE60", 
            "Prestado": "#F39C12", 
            "Archivo muerto": "#95A5A6"
        }
        color_estado = colores_estado.get(estado, "#7F8C8D")
        
        # Fila: Estado (destacado)
        estado_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        estado_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            estado_frame,
            text="📊 Estado:",
            font=("Segoe UI", 14, "bold"),
            text_color="#2C3E50",
            width=150,
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkLabel(
            estado_frame,
            text=estado,
            font=("Segoe UI", 14, "bold"),
            text_color=color_estado
        ).pack(side="left")
        
        # Separador
        ctk.CTkFrame(info_frame, fg_color="#E8E8E8", height=2).pack(fill="x", pady=8)
        
        # Datos en formato tabla
        datos = [
            ("📋 N° Expediente", f"#{fila[1]}"),
            ("📅 Fecha Nacimiento", fila[5]),
            ("⚤ Sexo", fila[6]),
            ("📍 Colonia", fila[7] if fila[7] else "—"),
            ("📅 Fecha Registro", fila[9]),
            ("🔄 Última Actualización", fila[10])
        ]
        
        for label, valor in datos:
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=4)
            
            ctk.CTkLabel(
                row_frame,
                text=label + ":",
                font=("Segoe UI", 13, "bold"),
                text_color="#2C3E50",
                width=160,
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                row_frame,
                text=valor,
                font=("Segoe UI", 13),
                text_color="#34495E"
            ).pack(side="left")
        
        # ===== PRÉSTAMO (si está prestado) =====
        if estado == "Prestado":
            prestamo = Prestamo.obtener_activo_por_expediente(fila[0])
            if prestamo:
                prestamo_frame = ctk.CTkFrame(main_frame, fg_color="#FFF3CD", corner_radius=10)
                prestamo_frame.pack(fill="x", padx=15, pady=10)
                
                ctk.CTkLabel(
                    prestamo_frame,
                    text="📤 INFORMACIÓN DEL PRÉSTAMO",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#856404"
                ).pack(pady=10)
                
                datos_prestamo = [
                    ("👤 Solicitado por:", prestamo[2]),
                    ("🏥 Área:", prestamo[3]),
                    ("📝 Motivo:", prestamo[4]),
                    ("📅 Fecha préstamo:", prestamo[5]),
                    ("⏰ Fecha límite:", prestamo[6])
                ]
                
                for label, valor in datos_prestamo:
                    row = ctk.CTkFrame(prestamo_frame, fg_color="transparent")
                    row.pack(fill="x", padx=15, pady=2)
                    
                    ctk.CTkLabel(
                        row,
                        text=label,
                        font=("Segoe UI", 12, "bold"),
                        text_color="#856404",
                        width=140,
                        anchor="w"
                    ).pack(side="left")
                    
                    ctk.CTkLabel(
                        row,
                        text=valor,
                        font=("Segoe UI", 12),
                        text_color="#856404"
                    ).pack(side="left")
        
        # ===== BOTONES DE ACCIÓN =====
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        if estado == "Disponible" and self.rol_actual != "Consulta":
            ctk.CTkButton(
                btn_frame,
                text="📤 Prestar Expediente",
                command=lambda: [ventana.destroy(), self._prestar(fila)],
                fg_color="#F39C12",
                hover_color="#D68910",
                width=160,
                height=40,
                font=("Segoe UI", 13, "bold")
            ).pack(side="left", padx=5)
        
        if estado == "Prestado" and self.rol_actual != "Consulta":
            ctk.CTkButton(
                btn_frame,
                text="📥 Registrar Devolución",
                command=lambda: [ventana.destroy(), self._devolver(fila)],
                fg_color="#27AE60",
                hover_color="#219150",
                width=160,
                height=40,
                font=("Segoe UI", 13, "bold")
            ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="📜 Ver Historial",
            command=lambda: [ventana.destroy(), self._ver_historial(fila)],
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            width=160,
            height=40,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🔙 Cerrar",
            command=ventana.destroy,
            fg_color="#95A5A6",
            hover_color="#7F8C8D",
            width=160,
            height=40,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left", padx=5)
    
    # ==========================================
    # REDIRECCIONES
    # ==========================================
    
    def _prestar(self, fila):
        print(f"📤 Redirigiendo a PRÉSTAMO - Expediente #{fila[1]}")
        try:
            self.principal.tabview.set("📤 PRÉSTAMO")
            if hasattr(self.principal, 'prestamo_view'):
                self.principal.prestamo_view.cargar_expediente(fila[1])
            else:
                messagebox.showerror("Error", "No se pudo abrir la ventana de préstamo")
        except Exception as e:
            print(f"❌ Error: {e}")
            messagebox.showerror("Error", f"Error al abrir préstamo: {str(e)}")
    
    def _devolver(self, fila):
        print(f"📥 Redirigiendo a DEVOLUCIÓN - Expediente #{fila[1]}")
        try:
            self.principal.tabview.set("📥 DEVOLUCIÓN")
            if hasattr(self.principal, 'devolucion_view'):
                self.principal.devolucion_view.cargar_expediente(fila[1])
            else:
                messagebox.showerror("Error", "No se pudo abrir la ventana de devolución")
        except Exception as e:
            print(f"❌ Error: {e}")
            messagebox.showerror("Error", f"Error al abrir devolución: {str(e)}")
    
    def _ver_historial(self, fila):
        print(f"📜 Redirigiendo a HISTORIAL - Expediente #{fila[1]}")
        try:
            self.principal.tabview.set("📜 HISTORIAL")
            if hasattr(self.principal, 'historial_view'):
                self.principal.historial_view.cargar_expediente(fila[1])
            else:
                messagebox.showerror("Error", "No se pudo abrir la ventana de historial")
        except Exception as e:
            print(f"❌ Error: {e}")
            messagebox.showerror("Error", f"Error al abrir historial: {str(e)}")
    
    def refrescar(self):
        self.buscar()