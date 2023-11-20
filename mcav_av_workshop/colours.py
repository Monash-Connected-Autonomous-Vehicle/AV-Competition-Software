"""
Colours used for colour detection
"""
import cv2
import numpy as np

RED = cv2.cvtColor(np.uint8([[[140, 15, 30]]]), cv2.COLOR_RGB2LAB)[0, 0, :]
SKY = cv2.cvtColor(np.uint8([[[110, 150, 180]]]), cv2.COLOR_RGB2LAB)[0, 0, :]
GREY = cv2.cvtColor(np.uint8([[[78, 82, 78]]]), cv2.COLOR_RGB2LAB)[0, 0, :]
GREEN = cv2.cvtColor(np.uint8([[[0, 128, 0]]]), cv2.COLOR_RGB2LAB)[0, 0, :]
WHITE = cv2.cvtColor(np.uint8([[[230, 240, 255]]]), cv2.COLOR_RGB2LAB)[0, 0, :]
BLUE = cv2.cvtColor(np.uint8([[[140, 200, 240]]]), cv2.COLOR_RGB2LAB)[0, 0, :]
