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
from vibration import Vibrators

camera = PiCamera()
sticker = Sticker()
darknet = Darknet()
qr = QR()
tts = TTS()
stt = STT()
vibrators = Vibrators()
            
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
            fifteen_up = 0.40*(Height/2)
            centre_upper = Height/2+fifteen_up
            centre_down = Height/2-fifteen_up
            change = 0
            if x==None or y==None:
                if len(points)!=0:
                    (x,y) = points[-1]
                    if int(x)>centre_region_begin and int(x)<=centre_region_end:
                        text = "NO CHANGE"
                    elif int(x)>centre_region_end and int(x)<=centre_region_end_part2:
                        text = "RIGHT"
                        change=1
                    elif int(x)>centre_region_end_part2:
                        text = "MORE RIGHT"
                        change=1
                    elif int(x)>=centre_region_begin_part2 and int(x)<=centre_region_begin:
                        text = "LEFT"
                        change=1
                    elif int(x)<centre_region_begin_part2:
                        text = "MORE LEFT"
                        change=1
                    if change==1:
                        if int(y)>centre_upper:
                            text+=" AND UP"
                        elif int(y)<centre_down:
                            text+=" AND DOWN"
                    if change==0:
                        if int(y)>centre_upper:
                            text+="UP"
                        elif int(y)<centre_down:
                            text+="DOWN"
                    print(text)
                    vibrators.set_profile(text)
                    tts.play_audio(text)
            else:
                if int(x)>centre_region_begin and int(x)<=centre_region_end:
                    text = "NO CHANGE"
                    vibrators.set_left(vibrators.OFF)
                    vibrators.set_right(vibrators.OFF)
                elif int(x)>centre_region_end and int(x)<=centre_region_end_part2:
                    text = "RIGHT"
                    vibrators.set_left(vibrators.OFF)
                    vibrators.set_right(vibrators.OFF)
                    change=1
                elif int(x)>centre_region_end_part2:
                    text = "MORE RIGHT"
                    change=1
                elif int(x)>=centre_region_begin_part2 and int(x)<=centre_region_begin:
                    text = "LEFT"
                    change=1
                elif int(x)<centre_region_begin_part2:
                    text = "MORE LEFT"
                    change=1
                if change==1:
                    if int(y)>centre_upper:
                        text+=" AND UP"
                    elif int(y)<centre_down:
                        text+=" AND DOWN"
                if change==0:
                    if int(y)>centre_upper:
                        text+="UP"
                    elif int(y)<centre_down:
                        text+="DOWN"
                print(text)
                vibrators.set_profile(text)
                tts.play_audio(text)
            break

def sticker_handler():
    print("Sticker Handler")
    points = []
    while True:
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        z,x,y = sticker.find_sticker(image)
        if z==False:
            continue
        points.append((x,y))
        text = ""
        Height, Width = image.shape[:2]
        fifteen_per = 0.40*(Width/2)
        centre_region_begin = Width/2-fifteen_per
        centre_region_end = Width/2+fifteen_per
        centre_region_begin_part2 = Width/2-2*fifteen_per
        centre_region_end_part2 = Width/2+2*fifteen_per
        fifteen_up = 0.40*(Height/2)
        centre_upper = Height/2+fifteen_up
        centre_down = Height/2-fifteen_up
        change = 0
        if x==None or y==None:
            if len(points)!=0:
                (x,y) = points[-1]
                if int(x)>centre_region_begin and int(x)<=centre_region_end:
                    text = "NO CHANGE"
                elif int(x)>centre_region_end and int(x)<=centre_region_end_part2:
                    text = "RIGHT"
                    change=1
                elif int(x)>centre_region_end_part2:
                    text = "MORE RIGHT"
                    change=1
                elif int(x)>=centre_region_begin_part2 and int(x)<=centre_region_begin:
                    text = "LEFT"
                    change=1
                elif int(x)<centre_region_begin_part2:
                    text = "MORE LEFT"
                    change=1
                if change==1:
                    if int(y)>centre_upper:
                        text+=" AND UP"
                    elif int(y)<centre_down:
                        text+=" AND DOWN"
                if change==0:
                    if int(y)>centre_upper:
                        text+="UP"
                    elif int(y)<centre_down:
                        text+="DOWN"
                print(text)
                vibrators.set_profile(text)
                tts.play_audio(text)
        else:
            if int(x)>centre_region_begin and int(x)<=centre_region_end:
                text = "NO CHANGE"
                vibrators.set_left(vibrators.OFF)
                vibrators.set_right(vibrators.OFF)
            elif int(x)>centre_region_end and int(x)<=centre_region_end_part2:
                text = "RIGHT"
                vibrators.set_left(vibrators.OFF)
                vibrators.set_right(vibrators.OFF)
                change=1
            elif int(x)>centre_region_end_part2:
                text = "MORE RIGHT"
                change=1
            elif int(x)>=centre_region_begin_part2 and int(x)<=centre_region_begin:
                text = "LEFT"
                change=1
            elif int(x)<centre_region_begin_part2:
                text = "MORE LEFT"
                change=1
            if change==1:
                if int(y)>centre_upper:
                    text+=" AND UP"
                elif int(y)<centre_down:
                    text+=" AND DOWN"
            if change==0:
                if int(y)>centre_upper:
                    text+="UP"
                elif int(y)<centre_down:
                    text+="DOWN"
            print(text)
            vibrators.set_profile(text)
            tts.play_audio(text)

def yolo_handler(name):
    print("Yolo Handler {}".format(name))
    points = []
    while True:
        found = False
        x = 0
        y = 0
        while found == False:
            rawCapture = PiRGBArray(camera)
            camera.capture(rawCapture, format="bgr")
            image = rawCapture.array
            arr, img = darknet.detect(image)
            print("Yolo Handler {}: {}".format(name, arr))
            flag = 0
            for elem in arr:
                print("{} {}".format(elem[0],name))
                if str.lower(elem[0]) == str.lower(name):
                    (x,y) = elem[2]
                    found = True
                    break
                else:
                    print("X: {} {}".format(elem[0], name))
        
       
        points.append((x,y))
        text = ""
        Height, Width = image.shape[:2]
        fifteen_per = 0.40*(Width/2)
        centre_region_begin = Width/2-fifteen_per
        centre_region_end = Width/2+fifteen_per
        centre_region_begin_part2 = Width/2-2*fifteen_per
        centre_region_end_part2 = Width/2+2*fifteen_per
        fifteen_up = 0.40*(Height/2)
        centre_upper = Height/2+fifteen_up
        centre_down = Height/2-fifteen_up
        change = 0
        print(x, y, "XY")
        if x==None or y==None:
            if len(points)!=0:
                (x,y) = points[-1]
                if int(x)>centre_region_begin and int(x)<=centre_region_end:
                    text = "NO CHANGE"
                elif int(x)>centre_region_end and int(x)<=centre_region_end_part2:
                    text = "RIGHT"
                    change=1
                elif int(x)>centre_region_end_part2:
                    text = "MORE RIGHT"
                    change=1
                elif int(x)>=centre_region_begin_part2 and int(x)<=centre_region_begin:
                    text = "LEFT"
                    change=1
                elif int(x)<centre_region_begin_part2:
                    text = "MORE LEFT"
                    change=1
                if change==1:
                    if int(y)>centre_upper:
                        text+=" AND UP"
                    elif int(y)<centre_down:
                        text+=" AND DOWN"
                if change==0:
                    if int(y)>centre_upper:
                        text+=" UP"
                    elif int(y)<centre_down:
                        text+=" DOWN"
                    print(text)
                    vibrators.set_profile(text)
                    tts.play_audio(text)
        else:
            if int(x)>centre_region_begin and int(x)<=centre_region_end:
                text = "NO CHANGE"
            elif int(x)>centre_region_end and int(x)<=centre_region_end_part2:
                text = "RIGHT"
                change=1
            elif int(x)>centre_region_end_part2:
                text = "MORE RIGHT"
                change=1
            elif int(x)>=centre_region_begin_part2 and int(x)<=centre_region_begin:
                text = "LEFT"
                change=1
            elif int(x)<centre_region_begin_part2:
                text = "MORE LEFT"
                change=1
            if change==1:
                if int(y)>centre_upper:
                    text+=" AND UP"
                elif int(y)<centre_down:
                    text+=" AND DOWN"
            if change==0:
                if int(y)>centre_upper:
                    text+=" UP"
                elif int(y)<centre_down:
                    text+=" DOWN"
            print(text)
            vibrators.set_profile(text)
            tts.play_audio(text)


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
        for name, _, centers in p_darknet.result()[0]:
            if name not in found_items:
                found_items.append((name, centers[0], centers[1]))
        print("{} Sticker:".format(iter))
        print(p_sticker.result())
        if p_sticker.result()[0]:
            found_items.append(("Sticker Found", p_sticker.result()[1], p_sticker.result()[2]))
        print("{} QR:".format(iter))
        for x, y, data in p_qr.result():
            print(x, y, data)
            if data not in found_items:
                found_items.append((data, x, y))

        for name, x, y in found_items:
            tts.play_audio(name)

        iter += 1

        # Wait for 3 second for user to give input
        user_command = str.lower(stt.voice_recognize(3))

    if user_command == "qr":
        qr_handler()
    elif user_command == "sticker":
        sticker_handler()
    else:
        closest_match = found_items[0][0]
        max_score = 0
        for ch in closest_match:
            if ch in user_command:
                max_score += 1
        for string, x, y in found_items:
            score = 0
            for ch in string:
                if ch in user_command:
                    score += 1
            if score > max_score:
                max_score = score
                closest_match = string

        yolo_handler(closest_match)
