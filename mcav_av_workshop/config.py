"""
Constants and configuration details for the AV workshop
"""
import numpy as np
import cv2


CAMERA_INTRINSIC = np.array([[1.26437615e+03, 0.00000000e+00, 6.39019835e+02],
                             [0.00000000e+00, 1.26346852e+03, 3.79144506e+02],
                             [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

# Radial Distortion Coefficients (k1, k2, k3, k4, k5, k6)
k1 = 0.01
k2 = -0.02
k3 = 0.003
k4 = 0.0001
k5 = -0.0005
k6 = 0.00001

# Tangential Distortion Coefficients (p1, p2)
p1 = 0.001
p2 = -0.002

# Thin Prism Distortion Coefficients (s1, s2, s3, s4)
s1 = 0.0001
s2 = -0.0002
s3 = 0.00003
s4 = 0.000005
CAMERA_DISTORTION = np.array([k1, k2, p1, p2, k3, k4, k5, k6, s1, s2, s3, s4])  # TODO: obtain distortion coefficients


ARUCO_SIZE = 0.1  # Width/height of ArUco markers, in meters
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)  # Use 4x4 dictionary to find markers
ARUCO_PARAMS = cv2.aruco.DetectorParameters()