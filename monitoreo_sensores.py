from pymata4 import pymata4

class Piso:
    def __init__(self, nombre, espacios_maximos):
        self.nombre = nombre
        self.espacios = espacios_maximos
        self.espacios_maximos = espacios_maximos

    def ocupar_lugar(self):
        if self.espacios > 0:
            self.espacios -= 1

    def devolver_lugar(self):
        if self.espacios < self.espacios_maximos:
            self.espacios += 1

# Simulación de sensores
planta_baja = Piso("Planta Baja", 22)
piso_1 = Piso("Primer Piso", 42)

def actualizar_ocupacion(deteccion):
    if deteccion:
        planta_baja.ocupar_lugar()
    else:
        planta_baja.devolver_lugar()
    return planta_baja.espacios
