import tkinter as tk
from tkinter import messagebox

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi página web interactiva")
ventana.geometry("600x400")
ventana.config(bg="#6A0DAD")  # morado de fondo

# Encabezado
encabezado = tk.Label(ventana, text="¡Bienvenido a mi página!", 
                      font=("Helvetica", 24, "bold"), bg="#6A0DAD", fg="#FFD700")  # amarillo
encabezado.pack(pady=20)

# Área donde aparecerá el texto agregado
texto_area = tk.Label(ventana, text="", font=("Arial", 14), bg="#6A0DAD", fg="#FFD700", wraplength=500)
texto_area.pack(pady=10)

# Texto que se agregará
mensaje_a_agregar = "¡Felicidades! Has agregado un mensaje a la ventana. 😃\nBienvenido a esta mini página interactiva."

# Función para agregar texto
def agregar_texto():
    texto_area.config(text=mensaje_a_agregar)

# Función para salir
def salir():
    ventana.destroy()

# Función mini-juego
def mini_juego():
    messagebox.showinfo("Mini-juego", "¡Mini-juego en construcción!")

# Crear los botones
boton_agregar = tk.Button(ventana, text="Agregar Texto", font=("Arial", 14, "bold"),
                          bg="#FFD700", fg="#6A0DAD", command=agregar_texto)
boton_agregar.pack(pady=10)

boton_entrar = tk.Button(ventana, text="Entrar al Mini-juego", font=("Arial", 14, "bold"),
                         bg="#FFD700", fg="#6A0DAD", command=mini_juego)
boton_entrar.pack(pady=10)

boton_salir = tk.Button(ventana, text="Salir", font=("Arial", 14, "bold"),
                        bg="#FFD700", fg="#6A0DAD", command=salir)
boton_salir.pack(pady=10)

# Pie de página
footer = tk.Label(ventana, text="© 2026 Mi Página Web", font=("Arial", 10),
                  bg="#6A0DAD", fg="#FFD700")
footer.pack(side="bottom", pady=10)

# Mostrar ventana
ventana.mainloop()