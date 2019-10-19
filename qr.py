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
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            print("YES")
            f_x = x+(w/2)
            f_y = y+(h/2)
            print((f_x,f_y))
            yield (f_x,f_y,barcodeData)

