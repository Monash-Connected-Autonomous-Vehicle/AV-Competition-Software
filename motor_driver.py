import picamera
import picamera.array
import sys
import numpy as np
from time import sleep
import RPi.GPIO as GPIO
from classes import Vehicle, Channel

#Pinmode, GPIO17 is referenced as 17
GPIO.setmode(GPIO.BCM)
#Setup each channel seperately
right_channel = Channel(2, 3, 4) #enable, fw, bk
left_channel = Channel(17, 27, 22)  #enable, fw, bk

#Control vehicle as a whole, or access instance variables to control right or left seperately
car = Vehicle(right_channel, left_channel)


#initialisation of camera
if True:
    with picamera.PiCamera() as camera:
        while True:
            camera.resolution = (128, 128)
            camera.framerate = 30
            output = np.empty((128,128,3), dtype=np.uint8)
            camera.capture(output, 'rgb')
            acc = 0
            n = output[:,:,0].size
            acc = np.sum(output[:,:, 0])
            # for i in output[0]:
            #     acc += int(i[0])
            #     n += 1
            print(type(acc))
            redness = acc/n

            print(f'redness = {redness} out of 256')
            if redness > 130:
                car.stop()
            else:
                car.drive(100, 'fw')

            #sleep(0.2)





    """ what callum wrote incase i break it 
    with picamera.array.PiRGBArray(camera) as output:               
        while True:

            camera.capture(output, 'rgb')
            arr = output.array
            #Define crop
            #Access pixels within crop
            #Count colour function
            #Make decisions
            #Move car
            print(arr)
            sleep(5)
        """



#There exists inconsistency between the different motor models when stepping through these steps
#Right channel seems to be able to handle a lower duty cycle than left
#Increasing the PWM frequency might help with this, however needs more thought
if False:
    car.left.stop()
    car.right.stop()
    #car.right.drive(80, 'fw')
   