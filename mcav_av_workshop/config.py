"""
Constants and configuration details for the AV workshop
"""
import numpy as np
import cv2


CAMERA_INTRINSIC = np.array([[1.26437615e+03, 0.00000000e+00, 6.39019835e+02],
                             [0.00000000e+00, 1.26346852e+03, 3.79144506e+02],
                             [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
CAMERA_DISTORTION = None  # TODO: obtain distortion coefficients


ARUCO_SIZE = 0.1  # Width/height of ArUco markers, in meters
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)  # Use 4x4 dictionary to find markers
ARUCO_PARAMS = cv2.aruco.DetectorParameters_create()