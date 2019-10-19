from darknet import Darknet
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
sticker = Darknet()

while True:
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    found, img = sticker.detect(image)
    cv2.imshow("wlekf", img)
    if cv2.waitKey(1) == 13:
        break
    print(found)

