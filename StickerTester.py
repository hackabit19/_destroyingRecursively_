from Sticker import Sticker
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
sticker = Sticker()

while True:
    sleep(0.5)
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    found, x, y = sticker.find_sticker(image, True)
    print(found)

