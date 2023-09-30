"""
The file that can be called with `python3 run.py` to run the robot
"""

import cv2
import argparse
import picamera
import sys
import numpy as np
from time import sleep
import RPi.GPIO as GPIO

from mcav_av_workshop.driving_tools import Vehicle, MotorChannel
from mcav_av_workshop import config
from behaviour import camera_response


def main(args):
    # Pinmode, GPIO17 is referenced as 17
    GPIO.setmode(GPIO.BCM)

    # Setup each MotorChannel seperately
    right_MotorChannel = MotorChannel(2, 3, 4)            # enable, fw, bk
    left_MotorChannel = MotorChannel(17, 27, 22)          # enable, fw, bk
    car = Vehicle(right_MotorChannel, left_MotorChannel)  # Control vehicle as a whole, or access instance variables to control right or left seperately

    # Setup camera image undistortion
    rect_mat, roi = cv2.getOptimalNewCameraMatrix(config.CAMERA_INTRINSIC, config.CAMERA_DISTORTION, 
                                                  args.resolution, 1, args.resolution)
    mapx, mapy = cv2.initUndistortRectifyMap(config.CAMERA_INTRINSIC, config.CAMERA_DISTORTION, 
                                             None, rect_mat, args.resolution, 5)

    # Set up Pi camera and run main loop
    with picamera.PiCamera(resolution=args.resolution, framerate=args.framerate) as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            for img in camera.capture_continuous(stream, format='rgb', use_video_port=True):
                rect_img = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
                
                # TODO: package img.array into our format for image slices
                lin_vel, ang_vel = camera_response(rect_img.array)
                # TODO: use lin_vel, ang_vel to drive car/Vehicle object
                car.drive_linang(lin_vel, ang_vel)

                # TODO: stop condition with Pi pin/switch
                
                # Flush stream buffer
                stream.truncate()
                stream.seek(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the robot for the AV competition')
    parser.add_argument('--resolution', default=(128, 128), type=tuple, help='Resolution of the vehicle\'s camera')
    parser.add_argument('--framerate', default=10, type=int, help='Frame rate of the vehicle\'s camera (fps)')
    args = parser.parse_args()

    main(args=args)

