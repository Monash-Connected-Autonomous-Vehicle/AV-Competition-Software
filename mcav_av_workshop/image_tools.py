"""
Image related operations for the AV workshop.
"""

import numpy as np
import cv2
from cv2 import aruco, COLOR_BGR2GRAY

from mcav_av_workshop import config




def aruco_pos(image):
    """
    Find position of visible ArUco markers in image, relative to vehicle
    """
    gray_image = cv2.cvtColor(image, COLOR_BGR2GRAY)  # Change grayscale
    corners, ids, _ = aruco.detectMarkers(gray_image, config.ARUCO_DICT, parameters=config.ARUCO_PARAMS)

    rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, config.ARUCO_SIZE, config.CAMERA_INTRINSIC, config.CAMERA_DISTORTION)

    # TODO: return relative position of aruco markers
          