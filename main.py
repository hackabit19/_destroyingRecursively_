from darknet import Darknet
from qr import QR 
from sticker import Sticker
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2
from concurrent.futures import ThreadPoolExecutor

camera = PiCamera()
sticker = Sticker()
darknet = Darknet()
qr = QR()

while True:
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    with ThreadPoolExecutor() as executor:
        p_darknet = executor.submit(darknet.detect, image)
        p_sticker = executor.submit(sticker.find_sticker, image)
        p_qr = executor.submit(qr.scan, image)
        print("Darknet:")
        print(p_darknet.result()[0])
        print("Sticker:")
        print(p_sticker.result())
        print("QR:")
        print(p_qr.result())