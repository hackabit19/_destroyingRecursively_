from pyzbar import pyzbar
import cv2
import numpy as np
import sys

class QR:
    def scan(self, frame):
        Height, Width = frame.shape[:2]
        img = frame
        barcodes = pyzbar.decode(img)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            f_x = x+(w/2)
            f_y = y+(h/2)
            yield (f_x,f_y,barcodeData)



