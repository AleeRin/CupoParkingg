import cv2 as cv
from deteccion_yolo import detectar_vehiculos
from monitoreo_sensores import planta_baja, actualizar_ocupacion
from interfaz import crear_interfaz

# Configuración de la cámara
cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

# Interfaz gráfica
root, actualizar_interfaz = crear_interfaz(planta_baja)

def procesar_camara():
    is_successful, frame = cam.read()
    if is_successful:
        frame_anotado, deteccion = detectar_vehiculos(frame)
        espacios = actualizar_ocupacion(deteccion)
        actualizar_interfaz(espacios)
        cv.imshow("YOLO Detección", frame_anotado)

    root.after(10, procesar_camara)

# Bucle principal
root.after(10, procesar_camara)
root.mainloop()
cam.release()
cv.destroyAllWindows()
