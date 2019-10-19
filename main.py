from darknet import Darknet
from qr import QR 
from sticker import Sticker
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2
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
    print(text)
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
