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

found_items = []
is_guide_engaged = False
def explore():
    iter = 1
    with ThreadPoolExecutor() as executor:
        while True:
            sleep(5)
            if not is_guide_engaged:
                rawCapture = PiRGBArray(camera)
                camera.capture(rawCapture, format="bgr")
                image = rawCapture.array

                p_darknet = executor.submit(darknet.detect, image)
                p_sticker = executor.submit(sticker.find_sticker, image)
                p_qr = executor.submit(qr.scan, image) 

                if not is_guide_engaged:
                    print("{} Darknet:".format(iter))
                    print(p_darknet.result()[0])        
                    for name, _, _ in p_darknet.result()[0]:
                        if name not in found_items:
                            found_items.append(name)

                if not is_guide_engaged:
                    print("{} Sticker:".format(iter))
                    print(p_sticker.result())
                    if p_sticker.result()[0]:
                        found_items.append("Sticker Found")

                if not is_guide_engaged:
                    print("{} QR:".format(iter))
                    for x, y, data in p_qr.result():
                        print(x, y, data)
                        if data not in found_items:
                            found_items.append(data)
                
                if not is_guide_engaged:
                    for name in found_items:
                        tts.play_audio(name)

                iter += 1


def do_something(text):
    sleep(2)
    if text=="QR":
        points = []
        while True:
            rawCapture = PiRGBArray(camera)
            camera.capture(rawCapture, format="bgr")
            image = rawCapture.array
            x=0
            y=0
            for x1,y1,_1 in qr.scan(image):
                x=x1,y=y1,_=_1
                break
            blank_image = np.zeros((image.shape[0], image.shape[1], 3))
            cv2.circle(blank_image, (int(x), int(y)), 20 ,(0, 0, 255), 2)
            cv2.circle(blank_image, (int(x), int(y)), 5, (0, 255, 0), -1)
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
                tts.play_audio(text)
            cv2.imshow("Object Tracker", blank_image)
            if cv2.waitKey(1) == 13: #13 is the Enter Key
                break
    sleep(10)

with ThreadPoolExecutor() as executor:
    explore_thread = executor.submit(explore)
    while True:
        print("Starting New Record")
        text = stt.voice_recognize(3)
        print("Ended Record")
        if len(text) > 0:
            is_guide_engagd = True
            sound_play = executor.submit(tts.play_audio, "Ok I'll guide you to {}".format(text))
            guide_thread = executor.submit(do_something, text)
            guide_thread.result()
            is_guide_engaged = False
