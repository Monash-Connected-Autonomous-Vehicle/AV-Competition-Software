"""
Image related operations for the AV workshop.
"""

import numpy as np
from matplotlib import pyplot as plt
import cv2

RED = (0, 255, 255)  # HSV representation of red, more colors can be added in future


def highlight_color(image, color, range_h=90, range_s=80, range_v=80):
    """
    Produces a binary image that is true when a given image is within a certain HSV range of a color.

    image: TODO: convert this to image abstraction
    color: RGB tuple for target color
    range_h: Tolerance for accepted hues (hues range from 0-360)
    range_s: Tolerance for accepted saturation (0-100)
    range_v: Tolerance for accepted value (0-100)
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # Find range values for saturation and value
    min_s, max_s = max(0, color[1]-range_s), min(255, color[1]+range_s)
    min_v, max_v = max(0, color[2]-range_v), min(255, color[2]+range_v)

    # Find range values for hue 
    if range_h >= 180:
        min_h, max_h = 0, 360

    else:
        min_h, max_h = color[0]-range_h, color[0]+range_h
        offset = 180 if color[0] < range_h else -180 if color[0] + range_h > 180 else 0
        if offset != 0:
            hsv[:,:,0] += offset
            min_h += offset
            max_h += offset

    return cv2.inRange(hsv, (min_h, min_s, min_v), (max_h, max_s, max_v))


if __name__ == '__main__':
    """
    Junk testing code can go here, this file should never be called directly in normal operation
    """
    test_img = cv2.imread('test/STOP.jpg')
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    test = highlight_color(test_img, RED)
    print(np.count_nonzero(test))
    plt.imshow(test)
    plt.show()


