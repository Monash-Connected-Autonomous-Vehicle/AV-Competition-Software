"""
Image related operations for the AV workshop.
"""

import numpy as np
from matplotlib import pyplot as plt
import cv2

# Various colors that can be used as defaults by participants
RED  = cv2.cvtColor(np.uint8([[[255, 0,   0  ]]]), cv2.COLOR_RGB2LAB)[0,0,:]  # A better red could be found for the application, interseting problem for participants!
SKY  = cv2.cvtColor(np.uint8([[[110, 150, 180]]]), cv2.COLOR_RGB2LAB)[0,0,:]
GREY = cv2.cvtColor(np.uint8([[[78,  82,  78 ]]]), cv2.COLOR_RGB2LAB)[0,0,:]


class Image:
    """ Dummy class for code layout planning """
    def __init__(self, img) -> None:
        self.img = img


class HighlightedImage(Image):
    """ Dummy class for code layout planning """
    def __init__(self, bin_img, color) -> None:
        super().__init__(bin_img)
        self.color = color


def highlight_color(image, color, thresh):
    """
    Produces a binary image of which pixels in a given image are close to a specified color.

    Color proximity is determined by the L1 norm distance between colors in LAB colorspace.

    Arguments
    ---------
    image : Image
        Image object containing uint8 representation of LAB colorspace image
    color : np.ndarray (uint8, uint8, uint8)
        LAB coordinate representation of highlighted color
    thresh : int
        L1 norm distance threshold for pixel color to be highlighted
    
    Returns
    -------
    highlighted_image : HighlightedImage
        Binary image of highlighted pixels with associated color

    Notes
    -----
    LAB colorspace is a perceptually uniform colorspace that better represents human color ituition than RGB.
    Perceptual uniformity is important when we want to use a single thresholding value for components.
    See morea bout LAB colorspace here: https://learnopencv.com/color-spaces-in-opencv-cpp-python/
    """
    color_low = np.where(color > thresh, color, thresh)-thresh
    color_high = np.where(color < 255-thresh, color, 255-thresh)+thresh

    return HighlightedImage(cv2.inRange(image, color_low, color_high), color)



if __name__ == '__main__':
    """
    Junk testing code can go here, this file should never be called directly in normal operation
    """
    test_img = cv2.imread('test/STOP.jpg')
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2LAB)

    
    test = highlight_color(test_img, GREY, 20)

    
    print(np.count_nonzero(test.img))
    plt.imshow(test.img)
    plt.show()


