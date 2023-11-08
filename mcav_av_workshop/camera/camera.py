from picamera2 import Picamera2
import time
import cv2 
import matplotlib.pyplot as plt
import numpy as np

# Define the Camera Variable 
picam2 = Picamera2()
# Initiate the PiCamera
picam2.start()
time.sleep(1)

# Request for the capturing of an image and convert it into array. 
array = picam2.capture_array("main")
print(array.shape)

#rgba = cv2.cvtColor(array, cv2.COLOR_RGB2RGBA)
plt.imshow(array)
plt.show()

