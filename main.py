from darknet import Darknet
from qr import QR 
from sticker import Sticker
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from text_to_speech import TTS
from speech_to_text import STT

camera = PiCamera()
sticker = Sticker()
darknet = Darknet()
qr = QR()
tts = TTS()
stt = STT()


# def do_something(text):
#     if text=="QR":
#         points = []
#         rawCapture = PiRGBArray(camera)
#         camera.capture(rawCapture, format="bgr")
#         image = rawCapture.array
#         blank_image = np.zeros((image.shape[0], image.shape[1], 3))
#         while True:
#             rawCapture = PiRGBArray(camera)
#             camera.capture(rawCapture, format="bgr")
#             image = rawCapture.array
#             for x,y,_ in qr.scan(image):
#                 cv2.circle(blank_image, (int(x), int(y)), 20 ,(0, 0, 255), 2)
#                 cv2.circle(blank_image, (int(x), int(y)), 5, (0, 255, 0), -1)
#                 points.append((x,y))
#                 text = ""
#                 Height, Width = image.shape[:2]
#                 fifteen_per = 0.40*(Width/2)
#                 centre_region_begin = Width/2-fifteen_per
#                 centre_region_end = Width/2+fifteen_per
#                 centre_region_begin_part2 = Width/2-2*fifteen_per
#                 centre_region_end_part2 = Width/2+2*fifteen_per
#                 if x==None or y==None:
#                     if len(points)!=0:
#                         (x,y) = points[-1]
#                         if int(x)>centre_region_begin and int(x)<=centre_region_end:
#                             text = "NO CHANGE"
#                         elif int(x)>centre_region_end and int(x)<=centre_region_end_part2:
#                             text = "RIGHT"
#                         elif int(x)>centre_region_end_part2:
#                             text = "MORE RIGHT"
#                         elif int(x)>=centre_region_begin_part2 and int(x)<=centre_region_begin:
#                             text = "LEFT"
#                         elif int(x)<centre_region_begin_part2:
#                             text = "MORE LEFT"
#                         #tts.play_audio(text)
#                         cv2.putText(blank_image, text, (int(x)+20, int(y)+20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),2)
#                 else:
#                     if int(x)>centre_region_begin and int(x)<=centre_region_end:
#                         text = "NO CHANGE"
#                     elif int(x)>centre_region_end and int(x)<=centre_region_end_part2:
#                         text = "RIGHT"
#                     elif int(x)>centre_region_end_part2:
#                         text = "MORE RIGHT"
#                     elif int(x)>=centre_region_begin_part2 and int(x)<=centre_region_begin:
#                         text = "LEFT"
#                     elif int(x)<centre_region_begin_part2:
#                         text = "MORE LEFT"
#                     cv2.putText(blank_image, text, (int(x)+20, int(y)+20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),2)
#                     #tts.play_audio(text)
#                 cv2.imshow("Object Tracker", blank_image)
#                 if cv2.waitKey(1) == 13: #13 is the Enter Key
#                     break
#                 break
            

def qr_handler():
    print("QR Handler")
    points = []
    while True:
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        for x,y,_ in qr.scan(image):
            points.append((x,y))
            text = ""
            Height, Width = image.shape[:2]
            fifteen_per = 0.40*(Width/2)
            centre_region_begin = Width/2-fifteen_per
            centre_region_end = Width/2+fifteen_per
            centre_region_begin_part2 = Width/2-2*fifteen_per
            centre_region_end_part2 = Width/2+2*fifteen_per
            if x==None or y==None:
                if len(points)!=0:
                    (x,y) = points[-1]
                    if int(x)>centre_region_begin and int(x)<=centre_region_end:
                        text = "NO CHANGE"
                    elif int(x)>centre_region_end and int(x)<=centre_region_end_part2:
                        text = "RIGHT"
                    elif int(x)>centre_region_end_part2:
                        text = "MORE RIGHT"
                    elif int(x)>=centre_region_begin_part2 and int(x)<=centre_region_begin:
                        text = "LEFT"
                    elif int(x)<centre_region_begin_part2:
                        text = "MORE LEFT"
                    print(text)
                    tts.play_audio(text)
            else:
                if int(x)>centre_region_begin and int(x)<=centre_region_end:
                    text = "NO CHANGE"
                elif int(x)>centre_region_end and int(x)<=centre_region_end_part2:
                    text = "RIGHT"
                elif int(x)>centre_region_end_part2:
                    text = "MORE RIGHT"
                elif int(x)>=centre_region_begin_part2 and int(x)<=centre_region_begin:
                    text = "LEFT"
                elif int(x)<centre_region_begin_part2:
                    text = "MORE LEFT"
                print(text)
                tts.play_audio(text)
            break

def sticker_handler():
    print("Sticker Handler")

def yolo_handler(name):
    print("Yolo Hanler {}".format(name))



iter = 1
user_command =  ""
with ThreadPoolExecutor() as executor:
    found_items = []
    while len(user_command) == 0:
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array

        p_darknet = executor.submit(darknet.detect, image)
        p_sticker = executor.submit(sticker.find_sticker, image)
        p_qr = executor.submit(qr.scan, image) 

        print("{} Darknet:".format(iter))
        print(p_darknet.result()[0])        
        for name, _, _ in p_darknet.result()[0]:
            if name not in found_items:
                found_items.append(name)
        print("{} Sticker:".format(iter))
        print(p_sticker.result())
        if p_sticker.result()[0]:
            found_items.append("Sticker Found")

        print("{} QR:".format(iter))
        for x, y, data in p_qr.result():
            print(x, y, data)
            if data not in found_items:
                found_items.append(data)

        for name in found_items:
            tts.play_audio(name)

        iter += 1

        # Wait for 3 second for user to give input
        user_command = str.lower(stt.voice_recognize(3))

    if user_command == "qr":
        qr_handler()
    elif user_command == "sticker":
        sticker_handler()
    else:
        yolo_handler(user_command)