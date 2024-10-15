import os
import cv2 as cv
from IDs import classes
from ultralytics import YOLO
#La funcion regresa un array con los nombres en ingles de todos los objetos que identifico en la imagen

def getObjetos(cv2Frame,visualize=False):
    numDeObjeto = 0
    palabrasEnTxt = []
    objetos = [] 
    model = YOLO("yolov8m.pt")
    model(cv2Frame,save=visualize,save_txt=True)
    #Leer txt y visualize
    pathToTxt = os.getcwd()
    pathToTxt += "\\runs\\detect\\predict\\labels\\image0.txt"
    try:
        with open(pathToTxt,"r") as text:
            palabrasEnTxt = text.read().replace("\n"," ")
            palabrasSeparadas = palabrasEnTxt.split(" ")
            text.close()
    except OSError:
        return "Error al leer el .txt"
    for palabra in palabrasSeparadas:
        palabra.strip()
        if numDeObjeto%5 == 0 and palabra.isnumeric():
            numero = int(palabra)
            objetos.append(classes.get(numero))
            numDeObjeto += 1
        else:
            numDeObjeto += 1
    if visualize:   
        pathToImg = os.getcwd()
        pathToImg += "\\runs\\detect\\predict\\image0.jpg"
        frame = cv.imread(pathToImg)
        cv.imshow("Camera",frame)
    #Borrar archivos temporales
    os.remove(pathToTxt)
    if visualize:
        os.remove(pathToImg)
    direcciones = pathToTxt.split("\\")
    for i in range(2):
        direcciones.pop(-1)
        newPath = ""
        primeraDireccion = True
        for direccion in direcciones:
            if primeraDireccion:
                newPath += direccion
                primeraDireccion = False
            else:
                newPath += "/"+direccion
        os.rmdir(newPath)
    return objetos