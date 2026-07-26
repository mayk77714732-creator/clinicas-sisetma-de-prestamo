"""
Vista de inicio de sesión - SIN LICENCIA
"""
import customtkinter as ctk
from tkinter import messagebox
from core.auth import Autenticacion
import traceback

class LoginView(ctk.CTkFrame):
    """Ventana de login del sistema"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.crear_interfaz()
        print("✅ LoginView cargado correctamente")
    
    def crear_interfaz(self):
        """Crea la interfaz de login"""
        self.login_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.login_frame.pack(expand=True, fill="both", padx=200, pady=100)
        
        # Título
        ctk.CTkLabel(
            self.login_frame,
            text="🏥 SISTEMA DE EXPEDIENTES",
            font=("Segoe UI", 28, "bold"),
            text_color="#1F6AA5"
        ).pack(pady=(40, 10))
        
        ctk.CTkLabel(
            self.login_frame,
            text="Inicio de Sesión",
            font=("Segoe UI", 16),
            text_color="#666"
        ).pack(pady=(0, 30))
        
        # Formulario
        form_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        form_frame.pack(pady=10)
        
        # Usuario
        ctk.CTkLabel(form_frame, text="Usuario:", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.usuario_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ingrese su usuario",
            width=300,
            height=40
        )
        self.usuario_entry.grid(row=1, column=0, pady=(0, 15))
        self.usuario_entry.focus()
        
        # Contraseña
        ctk.CTkLabel(form_frame, text="Contraseña:", font=("Segoe UI", 12, "bold")).grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ingrese su contraseña",
            width=300,
            height=40,
            show="*"
        )
        self.password_entry.grid(row=3, column=0, pady=(0, 15))
        
        # Rol
        ctk.CTkLabel(form_frame, text="Rol:", font=("Segoe UI", 12, "bold")).grid(
            row=4, column=0, sticky="w", pady=5
        )
        self.rol_combo = ctk.CTkComboBox(
            form_frame,
            values=["Administrador", "Personal de Archivo", "Consulta"],
            width=300,
            height=40
        )
        self.rol_combo.grid(row=5, column=0, pady=(0, 20))
        self.rol_combo.set("Personal de Archivo")
        
        # Botones
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=6, column=0)
        
        self.btn_login = ctk.CTkButton(
            btn_frame,
            text="🔑 Iniciar Sesión",
            command=self.iniciar_sesion,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=140,
            height=45,
            font=("Segoe UI", 14, "bold")
        )
        self.btn_login.pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ Salir",
            command=self.parent.destroy,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=140,
            height=45,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=5)
        
        # BARRA DE ESTADO
        self.status_label = ctk.CTkLabel(
            self.login_frame,
            text="✅ Ingrese sus credenciales",
            font=("Segoe UI", 11),
            text_color="gray"
        )
        self.status_label.pack(pady=10)
        
        # Atajos de teclado
        self.usuario_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.iniciar_sesion())
    
    def iniciar_sesion(self):
        """Valida las credenciales del usuario"""
        print("=" * 50)
        print("🔑 INICIANDO PROCESO DE LOGIN")
        print("=" * 50)
        
        try:
            self.btn_login.configure(text="⏳ Verificando...", state="disabled")
            self.status_label.configure(text="⏳ Verificando credenciales...", text_color="blue")
            self.update()
            
            usuario = self.usuario_entry.get().strip()
            password = self.password_entry.get().strip()
            rol = self.rol_combo.get()
            
            print(f"📝 Usuario: {usuario}")
            print(f"📝 Rol seleccionado: {rol}")
            
            if not usuario or not password:
                print("⚠️ Campos incompletos")
                messagebox.showwarning("Incompleto", "Complete todos los campos.")
                self.status_label.configure(text="⚠️ Complete todos los campos", text_color="orange")
                return
            
            # Verificar credenciales
            resultado = Autenticacion.verificar_credenciales(usuario, password)
            
            if resultado:
                print(f"✅ Login exitoso: {usuario}")
                self.status_label.configure(text=f"✅ Bienvenido {usuario}", text_color="green")
                
                rol_bd = resultado[3]
                print(f"📋 Rol en BD: {rol_bd}")
                
                self.btn_login.configure(text="🔑 Iniciar Sesión", state="normal")
                self.update()
                
                self.parent.iniciar_sistema(usuario, rol_bd)
            else:
                print("❌ Login fallido - Credenciales incorrectas")
                
                from core.database import Database
                conn = Database.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (usuario,))
                existe = cursor.fetchone()
                conn.close()
                
                if existe:
                    messagebox.showerror("Error", "Contraseña incorrecta.")
                    self.status_label.configure(text="❌ Contraseña incorrecta", text_color="red")
                else:
                    messagebox.showerror("Error", f"Usuario '{usuario}' no encontrado.")
                    self.status_label.configure(text="❌ Usuario no encontrado", text_color="red")
                
                self.password_entry.delete(0, 'end')
                self.password_entry.focus()
                self.btn_login.configure(text="🔑 Iniciar Sesión", state="normal")
                
        except Exception as e:
            print(f"❌ ERROR EN LOGIN: {e}")
            print(traceback.format_exc())
            messagebox.showerror(
                "Error de Login",
                f"Ocurrió un error al iniciar sesión:\n\n{str(e)}"
            )
            self.status_label.configure(text=f"❌ Error: {str(e)[:50]}", text_color="red")
            try:
                self.btn_login.configure(text="🔑 Iniciar Sesión", state="normal")
            except:
                pass
        
        finally:
            print("=" * 50)
            print("FIN DEL PROCESO DE LOGIN")
            print("=" * 50)