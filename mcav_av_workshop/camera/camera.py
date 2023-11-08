from picamera2 import Picamera2, Preview
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np

def capture_full_res(picam: Picamera2, output_file: str):
  capture_config = picam.create_still_configuration()
  picam.switch_mode_and_capture_file(capture_config, output_file)


if __name__ == '__main__':
  # Define the Camera Variable
  picam2 = Picamera2()

  # Preview
  picam2.start_preview(Preview.QTGL)
  preview_config = picam2.create_preview_configuration()
  picam2.configure(preview_config)

  # Initiate the PiCamera
  picam2.start()
  time.sleep(2)

  capture_full_res(picam=picam2, output_file="output_3.jpg")

  time.sleep(5)

  # # Request for the capturing of an image and convert it into array.
  # array = picam2.capture_array("main")
  # print(array.shape)

  # #rgba = cv2.cvtColor(array, cv2.COLOR_RGB2RGBA)
  # plt.imshow(array)
  # plt.show()