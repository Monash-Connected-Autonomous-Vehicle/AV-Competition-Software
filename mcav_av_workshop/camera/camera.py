from picamera2 import Picamera2
import time
import cv2 
import matplotlib.pyplot as plt
import numpy as np

# Define the Camera Variable 
picam2 = Picamera2()
## Achieved avg. 47FPS with this configuration, 3-6 buffers had the same speed, 1-2 were slower.
configuration = picam2.create_video_configuration(main={"size": (1920, 1080)},
                                                lores={"size": (640, 480)},
                                                controls={"FrameRate":60},
                                                buffer_count=6)
picam2.configure(configuration)
# Initiate the PiCamera
picam2.start()
time.sleep(1)

# Request for the capturing of an image and convert it into array. 
array = picam2.capture_array("main")
print(array.shape)

#rgba = cv2.cvtColor(array, cv2.COLOR_RGB2RGBA)
plt.imshow(array)
plt.show()

