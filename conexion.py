import psycopg2
from psycopg2 import Error
import tkinter as tk
from tkinter import messagebox, ttk
import hashlib

# --- CONFIGURACIÓN DE LA CONEXIÓN ---
DB_HOST = "localhost"
DB_NAME = "Jack"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_PORT = "5432"

def crear_conexion():
    try:
        return psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, 
            password=DB_PASSWORD, port=DB_PORT
        )
    except Error as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la BD:\n{e}")
        return None

def hashear_contrasena(password):
    return hashlib.sha256(password.encode()).hexdigest()

def crear_tablas_iniciales(conexion):
    """Crea la tabla de usuarios y la de productos si no existen"""
    try:
        cursor = conexion.cursor()
        
        # 1. Tabla de Usuarios
        query_usuarios = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            apellidos VARCHAR(100),
            correo VARCHAR(100) UNIQUE NOT NULL,
            telefono VARCHAR(20),
            contrasena VARCHAR(100) NOT NULL
        );"""
        cursor.execute(query_usuarios)

        # 2. Tabla de Productos
        query_productos = """
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            descripcion VARCHAR(200)
        );"""
        cursor.execute(query_productos)
        
        conexion.commit()
        cursor.close()
    except Error as e:
        print(f"Error al crear tablas: {e}")

def insertar_productos_ejemplo(conexion):
    """Inserta productos de prueba si la tabla está vacía"""
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT count(*) FROM productos")
        if cursor.fetchone()[0] == 0:
            productos = [
                ("Laptop HP Pavilion", 750.00, "Laptop para trabajo y estudio"),
                ("Mouse Inalámbrico", 15.50, "Ergonómico y recargable"),
                ("Teclado Mecánico", 45.00, "Luces RGB y switches azules"),
                ("Monitor 24 pulgadas", 120.00, "Full HD 60Hz"),
                ("Auriculares Gamer", 35.99, "Sonido envolvente y micrófono")
            ]
            query = "INSERT INTO productos (nombre, precio, descripcion) VALUES (%s, %s, %s)"
            cursor.executemany(query, productos)
            conexion.commit()
            print("Productos de ejemplo insertados.")
        cursor.close()
    except Error as e:
        print(f"Error insertando productos: {e}")

# --- LÓGICA DE REGISTRO ---
def funcion_registro():
    nombre = entry_nombre_reg.get()
    apellidos = entry_apellidos_reg.get()
    correo = entry_correo_reg.get()
    telefono = entry_telefono_reg.get()
    pass1 = entry_pass_reg.get()
    pass2 = entry_pass_confirm.get()

    if not nombre or not correo or not pass1:
        messagebox.showwarning("Campos vacíos", "Nombre, correo y contraseña son obligatorios.")
        return

    if pass1 != pass2:
        messagebox.showerror("Error", "Las contraseñas no coinciden.")
        return

    pass_hash = hashear_contrasena(pass1)

    try:
        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "INSERT INTO usuarios (nombre, apellidos, correo, telefono, contrasena) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (nombre, apellidos, correo, telefono, pass_hash))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "¡Usuario registrado correctamente!")
            ventana_registro.destroy()
    except Error as e:
        if "duplicate key" in str(e):
            messagebox.showerror("Error", "Ese correo electrónico ya está registrado.")
        else:
            messagebox.showerror("Error BD", f"Ocurrió un error: {e}")

# --- LÓGICA DE LOGIN ---
def funcion_login():
    correo = entry_correo_log.get()
    password = entry_pass_log.get()
    
    if not correo or not password:
         messagebox.showwarning("Campos vacíos", "Ingresa correo y contraseña.")
         return

    pass_hash = hashear_contrasena(password)

    try:
        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "SELECT nombre FROM usuarios WHERE correo = %s AND contrasena = %s"
            cursor.execute(query, (correo, pass_hash))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                nombre_usuario = resultado[0]
                ventana_raiz.withdraw() # Ocultar ventana de login
                abrir_tienda(nombre_usuario) # Abrir la tienda
            else:
                messagebox.showerror("Error", "Correo o contraseña incorrectos.")
    except Error as e:
        messagebox.showerror("Error", f"Error de base de datos: {e}")

# --- INTERFAZ GRÁFICA ---

def abrir_ventana_registro():
    global ventana_registro, entry_nombre_reg, entry_apellidos_reg, entry_correo_reg, entry_telefono_reg, entry_pass_reg, entry_pass_confirm
    
    ventana_registro = tk.Toplevel(ventana_raiz)
    ventana_registro.title("Registrarse")
    ventana_registro.geometry("350x400")

    tk.Label(ventana_registro, text="Crear Nueva Cuenta", font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(ventana_registro)
    frame.pack(pady=10)

    tk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre_reg = tk.Entry(frame, width=25)
    entry_nombre_reg.grid(row=0, column=1)

    tk.Label(frame, text="Apellidos:").grid(row=1, column=0, sticky="w", pady=5)
    entry_apellidos_reg = tk.Entry(frame, width=25)
    entry_apellidos_reg.grid(row=1, column=1)

    tk.Label(frame, text="Gmail/Correo:").grid(row=2, column=0, sticky="w", pady=5)
    entry_correo_reg = tk.Entry(frame, width=25)
    entry_correo_reg.grid(row=2, column=1)

    tk.Label(frame, text="Teléfono:").grid(row=3, column=0, sticky="w", pady=5)
    entry_telefono_reg = tk.Entry(frame, width=25)
    entry_telefono_reg.grid(row=3, column=1)

    tk.Label(frame, text="Contraseña:").grid(row=4, column=0, sticky="w", pady=5)
    entry_pass_reg = tk.Entry(frame, width=25, show="*")
    entry_pass_reg.grid(row=4, column=1)

    tk.Label(frame, text="Confirmar Contraseña:").grid(row=5, column=0, sticky="w", pady=5)
    entry_pass_confirm = tk.Entry(frame, width=25, show="*")
    entry_pass_confirm.grid(row=5, column=1)

    tk.Button(ventana_registro, text="Registrarse", bg="#4CAF50", fg="white", command=funcion_registro).pack(pady=20)

def comprar_producto(id_producto, nombre_producto):
    """Simula la compra de un producto"""
    # Aquí podrías guardar la compra en una tabla "ventas" si quisieras
    messagebox.showinfo("Compra Exitosa", f"¡Has comprado: {nombre_producto}!\n(ID: {id_producto})")

def abrir_tienda(nombre_usuario):
    """Ventana que muestra los productos disponibles"""
    ventana_tienda = tk.Toplevel()
    ventana_tienda.title("Tienda Virtual")
    ventana_tienda.geometry("500x450")

    # Cabecera de bienvenida
    tk.Label(ventana_tienda, text=f"Bienvenido, {nombre_usuario}", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(ventana_tienda, text="Productos Disponibles", font=("Arial", 12)).pack(pady=5)

    # Área de productos con scroll
    frame_lista = tk.Frame(ventana_tienda)
    frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

    # Canvas y Scrollbar para desplazarse si hay muchos productos
    canvas = tk.Canvas(frame_lista)
    scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Cargar productos desde la BD
    try:
        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, precio, descripcion FROM productos ORDER BY nombre")
            productos = cursor.fetchall()
            conexion.close()

            if not productos:
                tk.Label(scrollable_frame, text="No hay productos disponibles").pack()
            else:
                # Mostrar cada producto
                for prod in productos:
                    id_p, nombre_p, precio_p, desc_p = prod
                    
                    # Frame para cada fila de producto
                    fila_frame = tk.Frame(scrollable_frame, bd=1, relief="solid", padx=10, pady=5)
                    fila_frame.pack(fill="x", pady=5, padx=5)

                    # Información del producto
                    tk.Label(fila_frame, text=nombre_p, font=("Arial", 10, "bold")).pack(anchor="w")
                    tk.Label(fila_frame, text=f"Precio: ${precio_p:.2f}", fg="green").pack(anchor="w")
                    tk.Label(fila_frame, text=desc_p, fg="gray").pack(anchor="w")

                    # Botón Comprar
                    btn = tk.Button(fila_frame, text="Comprar", bg="#2196F3", fg="white",
                                    command=lambda id_p=id_p, nombre_p=nombre_p: comprar_producto(id_p, nombre_p))
                    btn.pack(anchor="e", pady=5)
                    
    except Error as e:
        messagebox.showerror("Error", f"No se pudieron cargar productos: {e}")

    tk.Button(ventana_tienda, text="Cerrar Sesión", command=ventana_tienda.destroy).pack(pady=10)

def iniciar_aplicacion():
    global ventana_raiz, entry_correo_log, entry_pass_log
    
    # 1. Crear la ventana principal PRIMERO
    ventana_raiz = tk.Tk()
    ventana_raiz.title("Sistema de Usuarios - Login")
    ventana_raiz.geometry("300x250")

    tk.Label(ventana_raiz, text="Iniciar Sesión", font=("Arial", 16, "bold")).pack(pady=20)

    frame_login = tk.Frame(ventana_raiz)
    frame_login.pack(pady=10)

    tk.Label(frame_login, text="Correo:").grid(row=0, column=0, padx=5, pady=5)
    entry_correo_log = tk.Entry(frame_login, width=20)
    entry_correo_log.grid(row=0, column=1, pady=5)

    tk.Label(frame_login, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)
    entry_pass_log = tk.Entry(frame_login, width=20, show="*")
    entry_pass_log.grid(row=1, column=1, pady=5)

    tk.Button(ventana_raiz, text="Entrar", width=15, bg="#2196F3", fg="white", command=funcion_login).pack(pady=10)
    tk.Button(ventana_raiz, text="Registrar nuevo usuario", command=abrir_ventana_registro).pack()

    # 2. Inicializar BD (Tablas y datos de ejemplo)
    conexion = crear_conexion()
    if conexion:
        crear_tablas_iniciales(conexion)
        insertar_productos_ejemplo(conexion) # Llenamos la tienda con ejemplos
        conexion.close()
    
    ventana_raiz.mainloop()

if __name__ == "__main__":
    iniciar_aplicacion()