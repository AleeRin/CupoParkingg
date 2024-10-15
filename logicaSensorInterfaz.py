from pymata4 import pymata4
import time
import tkinter as tk
from threading import Thread

# Configuración de la placa Arduino
board = pymata4.Pymata4(com_port='COM6', arduino_wait=8, baud_rate=57600)  # Inicializa la comunicación con la placa Arduino utilizando el puerto COM7 y otros parámetros para pymata

# Número de pines de sensores por piso
sensor_pins = {
    'planta_baja': [8],  # Define los pines de los sensores para el piso de la planta baja
    'piso_1': [9],  # Define los pines de los sensores para el primer piso
}

class Sensor:  
    def __init__(self, pin, piso, sensor_opuesto=None):  # Método de inicialización de la clase Sensor
        self.pin = pin  # Asigna el pin del sensor
        self.piso = piso  # Asigna el piso al que pertenece el sensor
        self.activo = False  # Estado inicial del sensor (no activo)
        self.sensor_opuesto = sensor_opuesto  # Sensor que será afectado cuando este sensor sea activado
        board.set_pin_mode_digital_input(self.pin)  # Configura el pin del sensor como entrada digital
    
    def leer_sensor(self):  # Método para leer el estado del sensor
        resultado = board.digital_read(self.pin)  # Lee el estado del pin digital
        lectura = resultado[0]  # Obtiene el valor de la lectura
        if lectura == 0:  # Si el sensor está activado
            if not self.activo:  # Si el sensor no estaba activo previamente
                self.activo = True  # Marca el sensor como activo
                if self.piso.espacios > 0:
                    self.piso.ocupar_lugar()  # Ocupa un lugar en el piso asociado
                if self.sensor_opuesto and self.sensor_opuesto.piso.espacios > 0:  # Si hay un sensor opuesto definido y hay espacios disponibles
                    self.sensor_opuesto.piso.devolver_lugar()  # Libera un lugar en el piso asociado al sensor opuesto
        elif lectura == 1 and self.activo:  # Si el sensor está desactivado y estaba activo previamente
            self.activo = False  # Marca el sensor como no activo
            self.piso.reset_primer_deteccion()  # Reinicia la detección inicial en el piso

class Piso:  
    def __init__(self, nombre, espacios, espacios_maximos):  
        self.nombre = nombre  # Nombre del piso
        self.espacios = espacios  # Número de espacios disponibles en el piso
        self.espacios_maximos = espacios_maximos  # Número máximo de espacios en el piso
        self.ultimo_cambio = time.time()  # Tiempo del último cambio en el piso
        self.primer_deteccion = False  # Indica si este piso fue detectado primero
    
    def ocupar_lugar(self):  
        if time.time() - self.ultimo_cambio > 1:  # Si ha pasado más de 1 segundo desde el último cambio
            if self.espacios > 0:
                self.espacios -= 1  # Reduce el número de espacios disponibles en el piso
                self.actualizar_interfaz()  # Actualiza la interfaz gráfica
                print(f"{self.nombre}: Espacios disponibles: {self.espacios}")  # Muestra la cantidad de espacios disponibles
            self.ultimo_cambio = time.time()  # Actualiza el tiempo del último cambio
    
    def devolver_lugar(self):  # Método para devolver un lugar en el piso
        if self.espacios < self.espacios_maximos:  # Si el número de espacios es menor que el máximo
            self.espacios += 1  # Incrementa el número de espacios disponibles en el piso
            self.actualizar_interfaz()  # Actualiza la interfaz gráfica
            print(f"{self.nombre}: Espacios devueltos: {self.espacios}")  # Muestra la cantidad de espacios devueltos
        self.ultimo_cambio = time.time()  # Actualiza el tiempo del último cambio
    
    def reset_primer_deteccion(self):  
        self.primer_deteccion = False  # Reinicia la variable que indica la detección inicial

    def actualizar_interfaz(self):
        if self.nombre == 'Planta Baja':
            planta_baja_label.config(text=f"Planta Baja: {self.espacios} espacios disponibles")
        elif self.nombre == 'Primer Piso':
            primer_piso_label.config(text=f"Primer Piso: {self.espacios} espacios disponibles")

# Creación de objetos para cada piso
planta_baja = Piso('Planta Baja', 22, 22)  # Crea un objeto Piso para la planta baja con 22 espacios disponibles
piso_1 = Piso('Primer Piso', 42, 42)  # Crea un objeto Piso para el primer piso con 42 espacios disponibles

# Creación de sensores asociados a cada piso
sensor_planta_baja = Sensor(sensor_pins['planta_baja'][0], planta_baja)  # Crea un sensor para la planta baja
sensor_piso_1 = Sensor(sensor_pins['piso_1'][0], piso_1, sensor_opuesto=sensor_planta_baja)  # Crea un sensor para el primer piso asociado con el sensor de la planta baja

sensores = [sensor_planta_baja, sensor_piso_1]  # Lista de sensores

def actualizar_sensores():
    try:
        while True:  # Bucle principal
            for sensor in sensores:  # Itera sobre cada sensor
                sensor.leer_sensor()  # Lee el estado del sensor
            time.sleep(0.1)  # Espera un breve tiempo para reducir la carga del CPU
    except KeyboardInterrupt:  # Manejo de interrupción del teclado
        print("Programa terminado por el usuario")  # Imprime un mensaje de finalización
    finally:  # Bloque de código que siempre se ejecuta al finalizar, independientemente de si hay una excepción o no
        # Cerrar la conexión correctamente
        board.shutdown()  # Cierra la conexión con la placa Arduino

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Sistema de Monitoreo de Sensores")
root.geometry("600x400")
root.configure(bg='darkgray')

title_label = tk.Label(root, text="Monitoreo de Estacionamiento", font=('Helvetica', 24, 'bold'), bg='darkgray', fg='navy')
title_label.pack(pady=20)

planta_baja_label = tk.Label(root, text=f"Planta Baja: {planta_baja.espacios} espacios disponibles", font=('Helvetica', 20), bg='gray', fg='black', width=40, height=2)
planta_baja_label.pack(pady=10)

primer_piso_label = tk.Label(root, text=f"Primer Piso: {piso_1.espacios} espacios disponibles", font=('Helvetica', 20), bg='gray', fg='black', width=40, height=2)
primer_piso_label.pack(pady=10)

footer_label = tk.Label(root, text="Sistema de Monitoreo en Tiempo Real", font=('Helvetica', 12), bg='black', fg='black')
footer_label.pack(side=tk.BOTTOM, pady=10)

# Iniciar el hilo para la actualización de los sensores
sensor_thread = Thread(target=actualizar_sensores)
sensor_thread.daemon = True
sensor_thread.start()

# Iniciar la interfaz gráfica
root.mainloop()
