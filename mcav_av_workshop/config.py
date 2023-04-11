"""
Constants and configuration details for the AV workshop
"""
import numpy as np
from cv2 import aruco

ARUCO_SIZE = 0.1
CAMERA_MATRIX = np.array([[1.26437615e+03, 0.00000000e+00, 6.39019835e+02],
                          [0.00000000e+00, 1.26346852e+03, 3.79144506e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

ARUCO_DICT = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)  # Use 4x4 dictionary to find markers
ARUCO_PARAMS = aruco.DetectorParameters_create()