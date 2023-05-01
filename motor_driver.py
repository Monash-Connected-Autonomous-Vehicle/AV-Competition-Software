import picamera
import picamera.array
from time import sleep
import RPi.GPIO as GPIO
from classes import Vehicle, Channel

#Pinmode, GPIO17 is referenced as 17
GPIO.setmode(GPIO.BCM)
#Setup each channel seperately
right_channel = Channel(14, 17, 18) #enable, fw, bk
left_channel = Channel(24, 22, 23)  #enable, fw, bk

#Control vehicle as a whole, or access instance variables to control right or left seperately
car = Vehicle(right_channel, left_channel)


#initialisation of camera
with picamera.PiCamera() as camera:
    camera.resolution = (128, 128)
    with picamera.array.PiRGBArray(camera) as output:
        while True:
            camera.capture(output, 'rgb')
            arr = output.array
            #Define crop
            #Access pixels within crop
            #Count colour function
            #Make decisions
            #Move car
            sleep(0.1)



#There exists inconsistency between the different motor models when stepping through these steps
#Right channel seems to be able to handle a lower duty cycle than left
#Increasing the PWM frequency might help with this, however needs more thought
if False:
    car.left.drive(60, 'fw')
    car.right.drive(80, 'bk')
    sleep(4)
    car.stop()
    car.drive(40, 'fw')
    sleep(3)
    car.stop()
    car.drive(70, 'bk')
    sleep(2)
    car.drive(90, 'fw')
    sleep(5)
    car.stop()
