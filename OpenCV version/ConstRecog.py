import cv2 as cv
from ObjectDetection import getObjetos

#Otra vez, funciona pero el framerate es horrible, para variar

cam=cv.VideoCapture(0)
while True:
    isSuccesful,frame = cam.read()
    print(getObjetos(frame,True))
    if cv.waitKey(10) & 0xFF == ord('q'):
        cam.release()
        cv.destroyAllWindows()
        break