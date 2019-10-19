from qr import QR
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2

camera = PiCamera()
#camera.resolution = (1640, 922)
qr = QR()

while True:
    sleep(0.5)
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, "bgr")
    image = rawCapture.array
    #cv2.imshow("name", image)
    #cv2.waitKey(0)
    for f_x, f_y, data in qr.scan(image):
        print(f_x, f_y, data)
