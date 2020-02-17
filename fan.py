# Fan control class

import RPi.GPIO as GPIO

SSR_pin = 37

class Fan():

    

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(SSR_pin, GPIO.OUT)
        
    def FanOn(self):
        GPIO.output(SSR_pin, 1)
 
    def FanOff(self):
        GPIO.output(SSR_pin, 0)


