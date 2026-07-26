"""
Vista de lista completa de expedientes - CON PAGINACIÓN
"""
import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from core.config import DB_PATH
from models.expediente import Expediente
from models.historial import Historial

class ListaView:
    """Vista para mostrar lista completa de expedientes con CRUD y paginación"""
    
    def __init__(self, parent, principal, usuario_actual, rol_actual):
        self.parent = parent
        self.principal = principal
        self.usuario_actual = usuario_actual
        self.rol_actual = rol_actual
        self.frame = None
        self.pagina_actual = 1
        self.por_pagina = 50
        self.total_paginas = 1
        self.datos_actuales = []
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de lista completa"""
        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título
        titulo_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        titulo_frame.pack(fill="x", pady=(10, 15))
        
        ctk.CTkLabel(
            titulo_frame,
            text="📋 LISTA COMPLETA DE EXPEDIENTES",
            font=("Segoe UI", 24, "bold"),
            text_color="#1F6AA5"
        ).pack(side="left")
        
        # Botones de acción
        if self.rol_actual != "Consulta":
            btn_frame = ctk.CTkFrame(titulo_frame, fg_color="transparent")
            btn_frame.pack(side="right")
            
            ctk.CTkButton(
                btn_frame,
                text="➕ NUEVO",
                command=self.abrir_registro,
                fg_color="#4CAF50",
                hover_color="#388E3C",
                width=100,
                height=35,
                font=("Segoe UI", 12, "bold")
            ).pack(side="left", padx=5)
            
            ctk.CTkButton(
                btn_frame,
                text="🔄 ACTUALIZAR",
                command=self.cargar_datos,
                fg_color="#3498DB",
                hover_color="#2980B9",
                width=100,
                height=35,
                font=("Segoe UI", 12, "bold")
            ).pack(side="left", padx=5)
        
        # Filtros y controles de paginación
        filtro_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        filtro_frame.pack(fill="x", pady=5)
        
        # Filtro de estado
        ctk.CTkLabel(filtro_frame, text="Filtrar por estado:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
        self.filtro_estado = ctk.CTkComboBox(
            filtro_frame,
            values=["Todos", "Disponible", "Prestado", "Archivo muerto"],
            width=150,
            height=35,
            command=self.cargar_datos
        )
        self.filtro_estado.pack(side="left", padx=5)
        self.filtro_estado.set("Todos")
        
        # Controles de paginación
        pag_frame = ctk.CTkFrame(filtro_frame, fg_color="transparent")
        pag_frame.pack(side="right", padx=10)
        
        self.btn_anterior = ctk.CTkButton(
            pag_frame,
            text="◀ Anterior",
            command=self.pagina_anterior,
            fg_color="#3498DB",
            hover_color="#2980B9",
            width=80,
            height=30,
            state="disabled"
        )
        self.btn_anterior.pack(side="left", padx=2)
        
        self.label_pagina = ctk.CTkLabel(
            pag_frame,
            text="Página 1 de 1",
            font=("Segoe UI", 12),
            text_color="#2C3E50"
        )
        self.label_pagina.pack(side="left", padx=10)
        
        self.btn_siguiente = ctk.CTkButton(
            pag_frame,
            text="Siguiente ▶",
            command=self.pagina_siguiente,
            fg_color="#3498DB",
            hover_color="#2980B9",
            width=80,
            height=30,
            state="disabled"
        )
        self.btn_siguiente.pack(side="left", padx=2)
        
        # Contador de registros
        self.contador_label = ctk.CTkLabel(
            filtro_frame,
            text="Total: 0 registros",
            font=("Segoe UI", 12),
            text_color="#7F8C8D"
        )
        self.contador_label.pack(side="right", padx=10)
        
        # Tabla de expedientes
        self.tabla_frame = ctk.CTkScrollableFrame(
            self.frame,
            fg_color="white",
            border_width=1,
            border_color="#BDC3C7",
            corner_radius=10
        )
        self.tabla_frame.pack(fill="both", expand=True, pady=10)
        
        # Crear encabezados
        self.crear_encabezados()
        
        # Cargar datos iniciales
        self.cargar_datos()
    
    def crear_encabezados(self):
        """Crea los encabezados de la tabla"""
        headers_frame = ctk.CTkFrame(self.tabla_frame, fg_color="#EAF2F8", height=35)
        headers_frame.pack(fill="x", pady=(0, 5))
        headers_frame.pack_propagate(False)
        
        columnas = [
            ("N°", 60),
            ("Nombre", 200),
            ("Apellido Paterno", 150),
            ("Apellido Materno", 150),
            ("Fecha Nac", 100),
            ("Sexo", 80),
            ("Colonia", 150),
            ("Estado", 100),
            ("Acciones", 200)
        ]
        
        for i, (texto, ancho) in enumerate(columnas):
            ctk.CTkLabel(
                headers_frame,
                text=texto,
                font=("Segoe UI", 12, "bold"),
                text_color="#2C3E50",
                width=ancho,
                anchor="w"
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
    
    def cargar_datos(self, *args):
        """Carga los datos de la tabla con paginación"""
        # Limpiar tabla (mantener encabezados)
        for widget in self.tabla_frame.winfo_children():
            if widget != self.tabla_frame.winfo_children()[0]:
                widget.destroy()
        
        filtro = self.filtro_estado.get()
        
        # Obtener datos paginados
        resultado = Expediente.obtener_paginado(filtro, self.pagina_actual, self.por_pagina)
        
        self.datos_actuales = resultado['datos']
        self.total_paginas = resultado['total_paginas']
        total = resultado['total']
        
        # Actualizar controles de paginación
        self.label_pagina.configure(text=f"Página {self.pagina_actual} de {self.total_paginas}")
        self.btn_anterior.configure(state="normal" if self.pagina_actual > 1 else "disabled")
        self.btn_siguiente.configure(state="normal" if self.pagina_actual < self.total_paginas else "disabled")
        self.contador_label.configure(text=f"Total: {total} registros")
        
        if not self.datos_actuales:
            ctk.CTkLabel(
                self.tabla_frame,
                text="📭 No hay expedientes registrados",
                font=("Segoe UI", 16),
                text_color="gray"
            ).pack(pady=50)
            return
        
        # Mostrar cada fila
        for fila in self.datos_actuales:
            self._crear_fila(fila)
        
        # Mostrar información de paginación
        info_text = f"Mostrando {len(self.datos_actuales)} de {total} registros"
        if self.total_paginas > 1:
            info_text += f" (Página {self.pagina_actual} de {self.total_paginas})"
        
        info_label = ctk.CTkLabel(
            self.tabla_frame,
            text=info_text,
            font=("Segoe UI", 11),
            text_color="#7F8C8D"
        )
        info_label.pack(pady=5)
    
    def pagina_anterior(self):
        """Va a la página anterior"""
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.cargar_datos()
    
    def pagina_siguiente(self):
        """Va a la página siguiente"""
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.cargar_datos()
    
    def _crear_fila(self, fila):
        """Crea una fila en la tabla"""
        row = ctk.CTkFrame(self.tabla_frame, fg_color="white", height=35)
        row.pack(fill="x", pady=1)
        row.pack_propagate(False)
        
        estado = fila[8]
        colores = {"Disponible": "#27AE60", "Prestado": "#F39C12", "Archivo muerto": "#95A5A6"}
        color_estado = colores.get(estado, "#7F8C8D")
        
        ctk.CTkLabel(row, text=str(fila[1]), width=60, anchor="w", font=("Segoe UI", 11)).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(row, text=fila[2], width=200, anchor="w", font=("Segoe UI", 11)).grid(row=0, column=1, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(row, text=fila[3], width=150, anchor="w", font=("Segoe UI", 11)).grid(row=0, column=2, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(row, text=fila[4] if fila[4] else "—", width=150, anchor="w", font=("Segoe UI", 11)).grid(row=0, column=3, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(row, text=fila[5], width=100, anchor="w", font=("Segoe UI", 11)).grid(row=0, column=4, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(row, text=fila[6], width=80, anchor="w", font=("Segoe UI", 11)).grid(row=0, column=5, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(row, text=fila[7] if fila[7] else "—", width=150, anchor="w", font=("Segoe UI", 11)).grid(row=0, column=6, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(row, text=estado, width=100, anchor="w", font=("Segoe UI", 11, "bold"), text_color=color_estado).grid(row=0, column=7, padx=5, pady=2, sticky="w")
        
        btn_frame = ctk.CTkFrame(row, fg_color="transparent")
        btn_frame.grid(row=0, column=8, padx=5, pady=2, sticky="w")
        
        ctk.CTkButton(
            btn_frame,
            text="👁️",
            width=30,
            height=25,
            fg_color="#3498DB",
            hover_color="#2980B9",
            command=lambda: self._ver_detalles(fila)
        ).pack(side="left", padx=2)
        
        if self.rol_actual != "Consulta":
            ctk.CTkButton(
                btn_frame,
                text="✏️",
                width=30,
                height=25,
                fg_color="#F39C12",
                hover_color="#D68910",
                command=lambda: self._editar_expediente(fila)
            ).pack(side="left", padx=2)
            
            if self.rol_actual == "Administrador":
                ctk.CTkButton(
                    btn_frame,
                    text="🗑️",
                    width=30,
                    height=25,
                    fg_color="#E74C3C",
                    hover_color="#C0392B",
                    command=lambda: self._eliminar_expediente(fila)
                ).pack(side="left", padx=2)
    
    def _ver_detalles(self, fila):
        """Muestra detalles del expediente"""
        nombre_completo = f"{fila[2]} {fila[3]} {fila[4]}".strip()
        messagebox.showinfo(
            "Detalles del Expediente",
            f"📋 EXPEDIENTE #{fila[1]}\n"
            f"{'='*40}\n\n"
            f"👤 Nombre: {nombre_completo}\n"
            f"📅 Fecha Nac: {fila[5]}\n"
            f"⚤ Sexo: {fila[6]}\n"
            f"📍 Colonia: {fila[7] if fila[7] else '—'}\n"
            f"📊 Estado: {fila[8]}\n"
            f"📅 Registrado: {fila[9]}\n"
            f"🔄 Actualizado: {fila[10]}"
        )
    
    def _editar_expediente(self, fila):
        """Abre el diálogo de edición"""
        ventana = ctk.CTkToplevel(self.parent)
        ventana.title(f"Editar Expediente #{fila[1]}")
        ventana.geometry("500x600")
        ventana.configure(fg_color="#F8F9FA")
        ventana.resizable(False, False)
        ventana.grab_set()
        
        main_frame = ctk.CTkScrollableFrame(ventana, fg_color="#F8F9FA")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text=f"✏️ EDITAR EXPEDIENTE #{fila[1]}",
            font=("Segoe UI", 20, "bold"),
            text_color="#1F6AA5"
        ).pack(pady=(0, 20))
        
        campos = [
            ("Nombre:", fila[2]),
            ("Apellido Paterno:", fila[3]),
            ("Apellido Materno:", fila[4] if fila[4] else ""),
            ("Fecha Nacimiento:", fila[5]),
            ("Sexo:", fila[6]),
            ("Colonia:", fila[7] if fila[7] else ""),
            ("Estado:", fila[8])
        ]
        
        entries = {}
        for i, (label, valor) in enumerate(campos):
            ctk.CTkLabel(main_frame, text=label, font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(10, 2))
            
            if label == "Sexo:":
                entry = ctk.CTkComboBox(main_frame, values=["Masculino", "Femenino"], width=400)
                entry.set(valor)
            elif label == "Estado:":
                entry = ctk.CTkComboBox(main_frame, values=["Disponible", "Prestado", "Archivo muerto"], width=400)
                entry.set(valor)
            else:
                entry = ctk.CTkEntry(main_frame, width=400)
                entry.insert(0, valor)
            
            entry.pack(pady=5)
            entries[label] = entry
        
        def guardar_edicion():
            nuevos_datos = {
                "Nombre:": entries["Nombre:"].get().strip().title(),
                "Apellido Paterno:": entries["Apellido Paterno:"].get().strip().title(),
                "Apellido Materno:": entries["Apellido Materno:"].get().strip().title(),
                "Fecha Nacimiento:": entries["Fecha Nacimiento:"].get().strip(),
                "Sexo:": entries["Sexo:"].get(),
                "Colonia:": entries["Colonia:"].get().strip(),
                "Estado:": entries["Estado:"].get()
            }
            
            if not nuevos_datos["Nombre:"] or not nuevos_datos["Apellido Paterno:"]:
                messagebox.showwarning("Incompleto", "Complete Nombre y Apellido Paterno.")
                return
            
            try:
                datetime.strptime(nuevos_datos["Fecha Nacimiento:"], "%d/%m/%Y")
            except:
                messagebox.showwarning("Fecha inválida", "La fecha debe tener formato DD/MM/AAAA")
                return
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE expedientes 
                SET nombre=?, apellido_paterno=?, apellido_materno=?, 
                    fecha_nacimiento=?, sexo=?, colonia=?, estado=?,
                    fecha_actualizacion=?
                WHERE id=?
            ''', (
                nuevos_datos["Nombre:"],
                nuevos_datos["Apellido Paterno:"],
                nuevos_datos["Apellido Materno:"],
                nuevos_datos["Fecha Nacimiento:"],
                nuevos_datos["Sexo:"],
                nuevos_datos["Colonia:"],
                nuevos_datos["Estado:"],
                datetime.now().strftime("%d/%m/%Y"),
                fila[0]
            ))
            conn.commit()
            conn.close()
            
            Historial.registrar(
                fila[0],
                "Edición",
                f"Expediente editado por {self.usuario_actual}",
                self.usuario_actual
            )
            
            messagebox.showinfo("Éxito", "Expediente actualizado correctamente.")
            ventana.destroy()
            self.cargar_datos()
        
        ctk.CTkButton(
            main_frame,
            text="💾 GUARDAR CAMBIOS",
            command=guardar_edicion,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=300,
            height=45,
            font=("Segoe UI", 14, "bold")
        ).pack(pady=20)
    
    def _eliminar_expediente(self, fila):
        """Elimina un expediente (solo Admin)"""
        nombre_completo = f"{fila[2]} {fila[3]} {fila[4]}".strip()
        
        if not messagebox.askyesno(
            "⚠️ Confirmar Eliminación",
            f"¿Está seguro de eliminar el expediente #{fila[1]}?\n\n"
            f"Paciente: {nombre_completo}\n\n"
            "⚠️ Esta acción NO se puede deshacer."
        ):
            return
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM historial WHERE id_expediente = ?", (fila[0],))
            cursor.execute("DELETE FROM prestamos WHERE id_expediente = ?", (fila[0],))
            cursor.execute("DELETE FROM expedientes WHERE id = ?", (fila[0],))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Éxito", f"Expediente #{fila[1]} eliminado correctamente.")
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")
    
    def abrir_registro(self):
        """Abre la pestaña de registro"""
        if hasattr(self.principal, 'tabview'):
            self.principal.tabview.set("📝 REGISTRO")