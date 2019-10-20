import RPi.GPIO as GPIO
from time import sleep

class Vibrators:
    def __init__(self, *args, **kwargs):
        self.leftPinGPIO = 12
        self.rightPinGPIO = 13
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.leftPinGPIO, GPIO.OUT)
        GPIO.setup(self.rightPinGPIO, GPIO.OUT)
        self.leftPwm = GPIO.PWM(self.leftPinGPIO, 100)
        self.rightPwm = GPIO.PWM(self.rightPinGPIO, 100)
        self.leftPwm.start(0)
        self.rightPwm.start(0)
        self.HIGH = 100
        self.MID = 50
        self.OFF = 0
        self.profiles = {
            "NO CHANGE": [self.OFF, self.OFF],
            "LEFT": [self.MID, self.OFF],
            "MORE LEFT": [self.HIGH, self.OFF],
            "RIGHT": [self.OFF, self.MID],
            "MORE RIGHT": [self.OFF, self.HIGH]
        }
    
    def set_left(self, magnitude):
        self.leftPwm.ChangeDutyCycle(magnitude)
    
    def set_right(self, magnitude):
        self.rightPwm.ChangeDutyCycle(magnitude)

    def set_profile(self, profile):
        if profile in self.profiles:
            self.set_left(self.profiles[profile][0])
            self.set_right(self.profiles[profile][1])
        else:
            print("Unsupported Profile")

if __name__ == "__main__":
    v = Vibrators()
    v.set_profile("LEFT")
    sleep(3)
    v.set_profile("NO CHANGE")
