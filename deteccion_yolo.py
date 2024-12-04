import cv2 as cv
from ultralytics import YOLO

# Inicializar YOLO
model = YOLO("yolov8n.pt")

def detectar_vehiculos(frame):
    results = model(frame)
    detecciones = results[0].boxes.data  # Obtiene datos de detección
    vehiculos_detectados = []

    for box in detecciones:
        clase = int(box[5])  # Índice de la clase detectada
        if clase in [2, 3]:  # Clases 'car' y 'motorcycle'
            vehiculos_detectados.append("vehiculo")  # Agrega un vehículo detectado
    
    # Devuelve la imagen anotada y las detecciones
    return results[0].plot(), len(vehiculos_detectados) > 0
