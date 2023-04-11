"""
Image related operations for the AV workshop.
"""

import numpy as np
import cv2
from cv2 import aruco, COLOR_BGR2GRAY

from mcav_av_workshop.config import ARUCO_SIZE, ARUCO_DICT, ARUCO_PARAMS, CAMERA_MATRIX

def aruco_pos(image):
    """
    Find position of visible ArUco markers in image, relative to vehicle
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Change grayscale
    corners, ids, _ = aruco.detectMarkers(gray_image, ARUCO_DICT, parameters=ARUCO_PARAMS)

    rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, ARUCO_SIZE, CAMERA_MATRIX, None)

    # TODO: return relative position of aruco markers
          