import picamera
import picamera.array
from time import sleep
import RPi.GPIO as GPIO

class Channel():
    def __init__(self, enable_pin, forward_pin, backward_pin):
        #Setting up pins
        GPIO.setup(enable_pin, GPIO.OUT)    #Enable
        GPIO.setup(forward_pin, GPIO.OUT)    #Foward
        GPIO.setup(backward_pin, GPIO.OUT)    #Backward
        #Setting output of enable to software PWM
        self.pwm = GPIO.PWM(enable_pin, 5000) #PWM on enable pin
        self.pwm.start(0)

        #GPIO pin numbers
        self.en = enable_pin
        self.fw = forward_pin
        self.bk = backward_pin
    
    def drive(self, duty_cycle:int, direction: str):
        #Set direction pin high, other low
        GPIO.output(self.fw, direction == 'fw')
        GPIO.output(self.bk, direction =='bk')

        #Change enable to PWM
        self.pwm.ChangeDutyCycle(duty_cycle)

    def stop(self):
        self.pwm.ChangeDutyCycle(0)

class Vehicle():
    def __init__(self, right: Channel, left: Channel):
        self.right = right
        self.left = left
    
    def turn(self,degrees):
        #Math for differential steering
        pass

    def stop(self):
        self.right.stop()
        self.left.stop()

    def drive(self, duty_cycle, direction):
        self.right.drive(duty_cycle, direction)
        self.left.drive(duty_cycle, direction)
