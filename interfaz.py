import tkinter as tk

def crear_interfaz(planta_baja):
    root = tk.Tk()
    root.title("Sistema de Monitoreo")
    planta_baja_label = tk.Label(root, text=f"Planta Baja: {planta_baja.espacios} espacios disponibles")
    planta_baja_label.pack()

    def actualizar_interfaz(espacios):
        planta_baja_label.config(text=f"Planta Baja: {espacios} espacios disponibles")

    return root, actualizar_interfaz
