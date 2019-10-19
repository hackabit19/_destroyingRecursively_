import RPi.GPIO as GPIO

class Vibrators:
    def __init__(self, *args, **kwargs):
        self.leftPinGPIO = 14
        self.rightPinGPIO = 15
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.leftPinGPIO, GPIO.OUT)
        GPIO.setup(self.rightPinGPIO, GPIO.OUT)

    def turn_left_on():
        GPIO.output(self.leftPinGPIO, GPIO.HIGH)
    
    def turn_left_off():
        GPIO.output(self.leftPinGPIO, GPIO.LOW)
    
    def turn_right_on():
        GPIO.output(self.rightPinGPIO, GPIO.HIGH)
    
    def turn_right_off():
        GPIO.output(self.rightPinGPIO, GPIO.LOW)