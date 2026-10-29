# login_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib


class LoginWindow:
    def __init__(self, root, db, on_login_success):
        self.root = root
        self.db = db
        self.on_login_success = on_login_success
        self.mostrar_password = False  # Estado para controlar si se muestra la contraseña
        self.usuario_actual = None  # Almacenar información del usuario

        self.root.title("Sistema de Mantenimiento de Vehículos - Login")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        # Centrar la ventana
        self.center_window()

        self.setup_ui()

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = 400
        height = 350
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def toggle_password_visibility(self):
        """Alterna entre mostrar y ocultar la contraseña"""
        self.mostrar_password = not self.mostrar_password

        if self.mostrar_password:
            self.password_entry.config(show="")
            self.toggle_btn.config(text="👁️ Ocultar")
        else:
            self.password_entry.config(show="•")
            self.toggle_btn.config(text="👁️ Mostrar")

    def setup_ui(self):
        # Marco principal
        main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Logo/título
        title_frame = tk.Frame(main_frame, bg="#f5f5f5")
        title_frame.pack(pady=(0, 30))

        tk.Label(title_frame, text="SISTEMA DE MANTENIMIENTO DE VEHÍCULOS",
                font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#2c3e50").pack()
        tk.Label(title_frame, text="Ingrese sus credenciales",
                font=("Arial", 10), bg="#f5f5f5", fg="#7f8c8d").pack(pady=(5, 0))

        # Formulario de login - Marco para centrar contenido
        form_container = tk.Frame(main_frame, bg="#f5f5f5")
        form_container.pack(expand=True, fill="both")

        # Marco interno para los campos (se centrará dentro del contenedor)
        form_frame = tk.Frame(form_container, bg="#f5f5f5")
        form_frame.pack(expand=True)

        # Usuario
        user_frame = tk.Frame(form_frame, bg="#f5f5f5")
        user_frame.pack(fill="x", pady=(0, 15))

        tk.Label(user_frame, text="Usuario:",
                font=("Arial", 10, "bold"), bg="#f5f5f5", fg="#34495e").pack(anchor="w")

        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(user_frame, textvariable=self.username_var, font=("Arial", 11), width=25)
        username_entry.pack(fill="x", pady=(5, 0))
        username_entry.focus()

        # Contraseña
        pass_frame = tk.Frame(form_frame, bg="#f5f5f5")
        pass_frame.pack(fill="x", pady=(0, 15))

        tk.Label(pass_frame, text="Contraseña:",
                font=("Arial", 10, "bold"), bg="#f5f5f5", fg="#34495e").pack(anchor="w")

        # Frame para campo de contraseña y botón de mostrar
        password_input_frame = tk.Frame(pass_frame, bg="#f5f5f5")
        password_input_frame.pack(fill="x", pady=(5, 0))

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_input_frame, textvariable=self.password_var, font=("Arial", 11),
                                      show="•", width=20)
        self.password_entry.pack(side="left", fill="x", expand=True)

        # Botón para mostrar/ocultar contraseña
        self.toggle_btn = tk.Button(password_input_frame, text="👁️ Mostrar",
                                  command=self.toggle_password_visibility,
                                  bg="#e74c3c", fg="white", font=("Arial", 9),
                                  padx=8, pady=2, relief="flat", cursor="hand2")
        self.toggle_btn.pack(side="right", padx=(5, 0))

        # Botón de login - Centrado
        button_container = tk.Frame(form_frame, bg="#f5f5f5")
        button_container.pack(fill="x", pady=(10, 0))

        login_btn = tk.Button(button_container, text="Iniciar Sesión", command=self.login,
                            bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                            padx=20, pady=8, cursor="hand2", relief="flat")
        login_btn.pack()

        # Enlace de enter para login
        username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        try:
            usuario = self.db.verificar_usuario(username, password)
            if usuario:
                # Almacenar información completa del usuario
                usuario_completo = self.db.obtener_usuario_por_id(usuario[0])
                self.usuario_actual = usuario_completo

                messagebox.showinfo("Éxito", f"Bienvenido, {usuario[2]}!")
                self.root.destroy()
                self.on_login_success(self.usuario_actual)  # Pasar información del usuario
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {str(e)}")
