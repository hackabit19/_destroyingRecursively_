import RPi.GPIO as GPIO
from time import sleep

class Vibrators:
    def __init__(self, *args, **kwargs):
        self.leftPinGPIO = 23
        self.rightPinGPIO = 24
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.leftPinGPIO, GPIO.OUT)
        GPIO.setup(self.rightPinGPIO, GPIO.OUT)

    def turn_left_on(self):
        GPIO.output(self.leftPinGPIO, GPIO.HIGH)
    
    def turn_left_off(self):
        GPIO.output(self.leftPinGPIO, GPIO.LOW)
    
    def turn_right_on(self):
        GPIO.output(self.rightPinGPIO, GPIO.HIGH)
    
    def turn_right_off(self):
        GPIO.output(self.rightPinGPIO, GPIO.LOW)

if __name__ == "__main__":
    v = Vibrators()
    v.turn_right_on()
    sleep(5)
    v.turn_right_off()
