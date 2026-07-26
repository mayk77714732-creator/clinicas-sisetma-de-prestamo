"""
Vista de configuración y gestión de usuarios - SIN LICENCIA
"""
import customtkinter as ctk
from tkinter import messagebox
import os
from core.auth import Autenticacion
from core.config import RESPALDOS_DIR, DB_PATH

class AjustesView:
    """Vista de configuración del sistema"""
    
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.ventana = None
    
    def mostrar(self):
        """Muestra la ventana de configuración"""
        self.ventana = ctk.CTkToplevel(self.parent)
        self.ventana.title("⚙️ Configuración del Sistema")
        self.ventana.geometry("700x650")
        self.ventana.configure(fg_color="#F8F9FA")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        
        main_frame = ctk.CTkFrame(self.ventana, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        tabview = ctk.CTkTabview(main_frame, width=650, height=550)
        tabview.pack(fill="both", expand=True)
        
        tab_usuarios = tabview.add("👤 USUARIOS")
        self._interfaz_usuarios(tab_usuarios)
        
        tab_seguridad = tabview.add("🔐 SEGURIDAD")
        self._interfaz_seguridad(tab_seguridad)
        
        tab_respaldo = tabview.add("💾 RESPALDO")
        self._interfaz_respaldo(tab_respaldo)
    
    def _interfaz_usuarios(self, parent):
        """Interfaz de gestión de usuarios"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame, text="Usuarios del Sistema", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=5)
        
        scroll_frame = ctk.CTkScrollableFrame(frame, height=300, fg_color="white", corner_radius=10)
        scroll_frame.pack(fill="both", expand=True, pady=5)
        
        usuarios = Autenticacion.obtener_usuarios()
        
        for usuario in usuarios:
            self._crear_tarjeta_usuario(scroll_frame, usuario)
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="➕ Agregar Usuario",
            command=self.agregar_usuario,
            fg_color="#27AE60",
            hover_color="#219150",
            width=150
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Restaurar Contraseña",
            command=self.restaurar_contrasena,
            fg_color="#F39C12",
            hover_color="#D68910",
            width=150
        ).pack(side="left", padx=5)
    
    def _crear_tarjeta_usuario(self, parent, usuario):
        id, usuario_nombre, rol, nombre_completo, fecha_reg, activo = usuario
        
        tarjeta = ctk.CTkFrame(parent, fg_color="#F8F9FA", corner_radius=8)
        tarjeta.pack(fill="x", pady=3, padx=5)
        
        estado_texto = "✅ Activo" if activo else "❌ Inactivo"
        estado_color = "#27AE60" if activo else "#E74C3C"
        
        info = f"👤 {usuario_nombre} ({rol})\n"
        info += f"📛 {nombre_completo}  |  📅 {fecha_reg}  |  {estado_texto}"
        
        ctk.CTkLabel(tarjeta, text=info, font=("Segoe UI", 12), 
                    text_color="#333", justify="left").pack(side="left", padx=10, pady=5)
        
        if activo:
            ctk.CTkButton(
                tarjeta,
                text="🔒 Desactivar",
                command=lambda: self.desactivar_usuario(id, usuario_nombre),
                fg_color="#E74C3C",
                hover_color="#C0392B",
                width=80
            ).pack(side="right", padx=5)
    
    def agregar_usuario(self):
        dialog = ctk.CTkToplevel(self.ventana)
        dialog.title("Agregar Usuario")
        dialog.geometry("400x400")
        dialog.configure(fg_color="#F8F9FA")
        dialog.grab_set()
        
        frame = ctk.CTkFrame(dialog, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Nuevo Usuario", font=("Segoe UI", 18, "bold")).pack(pady=10)
        
        ctk.CTkLabel(frame, text="Usuario:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        usuario_entry = ctk.CTkEntry(frame, placeholder_text="Nombre de usuario", width=300)
        usuario_entry.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Nombre completo:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        nombre_entry = ctk.CTkEntry(frame, placeholder_text="Nombre completo", width=300)
        nombre_entry.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Contraseña:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        pass_entry = ctk.CTkEntry(frame, placeholder_text="Contraseña", width=300, show="*")
        pass_entry.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Rol:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        rol_combo = ctk.CTkComboBox(frame, values=["Administrador", "Personal de Archivo", "Consulta"], width=300)
        rol_combo.set("Personal de Archivo")
        rol_combo.pack(pady=5)
        
        def guardar():
            usuario = usuario_entry.get().strip()
            nombre = nombre_entry.get().strip()
            contrasena = pass_entry.get().strip()
            rol = rol_combo.get()
            
            if not usuario or not nombre or not contrasena:
                messagebox.showwarning("Incompleto", "Complete todos los campos.")
                return
            
            if Autenticacion.crear_usuario(usuario, contrasena, rol, nombre):
                messagebox.showinfo("Éxito", f"Usuario {usuario} creado correctamente.")
                dialog.destroy()
                self.mostrar()
            else:
                messagebox.showerror("Error", "No se pudo crear el usuario.")
        
        ctk.CTkButton(frame, text="✅ Guardar", command=guardar,
                     fg_color="#4CAF50", hover_color="#388E3C", width=200).pack(pady=15)
    
    def desactivar_usuario(self, id_usuario, nombre):
        if messagebox.askyesno("Confirmar", f"¿Desactivar usuario '{nombre}'?"):
            if Autenticacion.desactivar_usuario(id_usuario):
                messagebox.showinfo("Éxito", f"Usuario {nombre} desactivado.")
                self.mostrar()
    
    def restaurar_contrasena(self):
        usuarios = Autenticacion.obtener_usuarios()
        nombres = [f"{u[1]} - {u[3]}" for u in usuarios]
        
        if not nombres:
            messagebox.showinfo("Info", "No hay usuarios registrados.")
            return
        
        dialog = ctk.CTkToplevel(self.ventana)
        dialog.title("Restaurar Contraseña")
        dialog.geometry("400x200")
        dialog.configure(fg_color="#F8F9FA")
        dialog.grab_set()
        
        frame = ctk.CTkFrame(dialog, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Seleccionar usuario:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        combo = ctk.CTkComboBox(frame, values=nombres, width=350)
        combo.pack(pady=10)
        combo.set(nombres[0] if nombres else "")
        
        def restaurar():
            seleccion = combo.get()
            if not seleccion:
                return
            
            usuario_nombre = seleccion.split(" - ")[0]
            if Autenticacion.restaurar_contrasena(usuario_nombre):
                messagebox.showinfo(
                    "Éxito",
                    f"Contraseña de {usuario_nombre} restaurada a '123456'."
                )
                dialog.destroy()
        
        ctk.CTkButton(frame, text="🔄 Restaurar", command=restaurar,
                     fg_color="#F39C12", hover_color="#D68910", width=200).pack(pady=10)
    
    def _interfaz_seguridad(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame, text="🔐 Cambiar Contraseña", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=5)
        
        ctk.CTkLabel(frame, text=f"Usuario: {self.usuario_actual}", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
        
        ctk.CTkLabel(frame, text="Nueva contraseña:", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
        nueva_pass = ctk.CTkEntry(frame, placeholder_text="Nueva contraseña", width=300, show="*")
        nueva_pass.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Confirmar contraseña:", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
        confirm_pass = ctk.CTkEntry(frame, placeholder_text="Confirmar contraseña", width=300, show="*")
        confirm_pass.pack(pady=5)
        
        def cambiar_pass():
            nueva = nueva_pass.get().strip()
            confirm = confirm_pass.get().strip()
            
            if not nueva:
                messagebox.showwarning("Incompleto", "Ingrese la nueva contraseña.")
                return
            
            if nueva != confirm:
                messagebox.showwarning("Error", "Las contraseñas no coinciden.")
                return
            
            if Autenticacion.cambiar_contrasena(self.usuario_actual, nueva):
                messagebox.showinfo("Éxito", "Contraseña cambiada correctamente.")
                nueva_pass.delete(0, 'end')
                confirm_pass.delete(0, 'end')
            else:
                messagebox.showerror("Error", "No se pudo cambiar la contraseña.")
        
        ctk.CTkButton(frame, text="✅ Cambiar Contraseña", command=cambiar_pass,
                     fg_color="#4CAF50", hover_color="#388E3C", width=250).pack(pady=15)
    
    def _interfaz_respaldo(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame, text="💾 Respaldos", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=5)
        
        ctk.CTkButton(frame, text="📁 Crear Respaldo", command=self.crear_respaldo,
                     fg_color="#27AE60", hover_color="#219150", width=250).pack(pady=5)
        
        ctk.CTkButton(frame, text="📂 Abrir Carpeta de Respaldos", 
                     command=lambda: os.startfile(RESPALDOS_DIR) if os.path.exists(RESPALDOS_DIR) else None,
                     fg_color="#2980B9", hover_color="#2471A3", width=250).pack(pady=5)
        
        info_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=10)
        info_frame.pack(fill="x", pady=10)
        self.mostrar_info_respaldo(info_frame)
    
    def mostrar_info_respaldo(self, parent):
        try:
            archivos = [f for f in os.listdir(RESPALDOS_DIR) if f.endswith('.zip')]
            archivos.sort(reverse=True)
            
            if archivos:
                ultimo = archivos[0]
                fecha = ultimo.replace("respaldo_expedientes_", "").replace(".zip", "").replace("_", " ").replace("-", "/")
                
                ctk.CTkLabel(parent, text=f"📅 Último respaldo: {fecha}", 
                            font=("Segoe UI", 12), text_color="#333").pack(anchor="w", padx=10, pady=2)
                ctk.CTkLabel(parent, text=f"📦 Respaldos disponibles: {len(archivos)}", 
                            font=("Segoe UI", 12), text_color="#333").pack(anchor="w", padx=10, pady=2)
            else:
                ctk.CTkLabel(parent, text="No hay respaldos disponibles", 
                            font=("Segoe UI", 12), text_color="#7F8C8D").pack(pady=10)
        except:
            ctk.CTkLabel(parent, text="Error al leer respaldos", 
                        font=("Segoe UI", 12), text_color="#E74C3C").pack(pady=10)
    
    def crear_respaldo(self):
        import zipfile
        from datetime import datetime
        
        try:
            fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nombre_zip = os.path.join(RESPALDOS_DIR, f"respaldo_expedientes_{fecha}.zip")
            with zipfile.ZipFile(nombre_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.exists(DB_PATH):
                    zipf.write(DB_PATH, os.path.basename(DB_PATH))
            messagebox.showinfo("Éxito", f"Respaldo creado:\n{nombre_zip}")
            self.mostrar()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear respaldo: {e}")