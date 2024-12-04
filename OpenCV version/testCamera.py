import cv2 as cv
from ultralytics import YOLO

# Cargar el modelo YOLO una vez fuera del bucle
model = YOLO("yolov8n.pt")  # Usa YOLOv8 Nano para mejor velocidad

# Configurar la cámara
cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)  # Reduce la resolución para mejor rendimiento
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    isSuccessful, frame = cam.read()
    if not isSuccessful:
        print("No se pudo acceder a la cámara.")
        break

    # Realizar la detección en el fotograma
    results = model(frame)

    # Obtener la imagen con anotaciones
    annotated_frame = results[0].plot()  # Dibuja las detecciones en el fotograma

    # Mostrar la imagen con detecciones
    cv.imshow("Detección de Objetos en Tiempo Real", annotated_frame)

    # Salir al presionar 'q'
    if cv.waitKey(10) & 0xFF == ord('q'):
        break

# Liberar recursos
cam.release()
cv.destroyAllWindows()
