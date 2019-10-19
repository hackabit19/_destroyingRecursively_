from darknet import Darknet
from qr import QR 
from sticker import Sticker
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2
from multiprocessing import Process

camera = PiCamera()
sticker = Sticker()
darknet = Darknet()
qr = QR()

while True:
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    p_darknet = Process(target=darknet.detect, args=(image))
    p_sticker = Process(target=sticker.find_sticker, args=(image))
    p_qr = Process(target=qr.scan, args=(image))
    p_darknet.join()
    p_sticker.join()
    p_qr.join()
    print("Darknet:")
    print(p_darknet.get()[0])
    print("Sticker:")
    print(p_sticker.get())
    print("QR:")
    print(p_qr.get())