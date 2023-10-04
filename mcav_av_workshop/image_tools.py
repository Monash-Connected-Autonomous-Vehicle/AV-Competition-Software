"""
Image related operations for the AV workshop.
"""

import numpy as np
import cv2
from cv2 import aruco
from matplotlib import pyplot as plt
    
from config import*


# Various colors that can be used as defaults by participants
RED  = cv2.cvtColor(np.uint8([[[140, 15, 30  ]]]), cv2.COLOR_RGB2LAB)[0,0,:]  # A better red could be found for the application, interseting problem for participants!
SKY  = cv2.cvtColor(np.uint8([[[110, 150, 180]]]), cv2.COLOR_RGB2LAB)[0,0,:]
GREY = cv2.cvtColor(np.uint8([[[78,  82,  78 ]]]), cv2.COLOR_RGB2LAB)[0,0,:]
GREEN = cv2.cvtColor(np.uint8([[[0, 128,    0]]]), cv2.COLOR_RGB2LAB)[0,0,:]
WHITE = cv2.cvtColor(np.uint8([[[230, 240,255]]]), cv2.COLOR_RGB2LAB)[0,0,:]
BLUE = cv2.cvtColor(np.uint8([[[140, 200, 240]]]), cv2.COLOR_RGB2LAB)[0,0,:] 

class Frame:
    """
    """
    def __init__(self, resolution) -> None:
        self.resolution = resolution
        self.camera_intrisic = CAMERA_INTRINSIC
        self.camera_distortion = CAMERA_DISTORTION

        self.rect_mat, self.roi = cv2.getOptimalNewCameraMatrix(CAMERA_INTRINSIC, CAMERA_DISTORTION, 
                                                                resolution, 1, resolution)
        self.mapx, self.mapy = cv2.initUndistortRectifyMap(CAMERA_INTRINSIC, CAMERA_DISTORTION, 
                                                           None, self.rect_mat, resolution, 5)
        
        self.image_lab = None
        self.image_gray = None


    def update_image(self, raw_image):
        rect_img = cv2.remap(raw_image, self.mapx, self.mapy, cv2.INTER_LINEAR)

        if self.image_lab is not None: self.image_lab[:] = cv2.cvtColor(rect_img, cv2.COLOR_RGB2LAB)  # Alter image in place if frame already initialized
        else: self.image_lab = cv2.cvtColor(rect_img, cv2.COLOR_RGB2LAB)

        if self.image_gray is not None: self.image_gray[:] = cv2.cvtColor(rect_img, cv2.COLOR_RGB2GRAY)
        else: self.image_gray = cv2.cvtColor(rect_img, cv2.COLOR_RGB2GRAY)
        

class Crop:
    """
    """
    def __init__(self, frame, slice) -> None:
        self.frame = frame
        self.slice = slice
    
    def __getitem__(self, overlay_slice):
        return Crop(self.frame, np.s_[Crop._compose_slices(self.slice[0], overlay_slice[0]), 
                                      Crop._compose_slices(self.slice[1], overlay_slice[1])], self.image)
        

    def aruco_pos(self):
        corners, ids, _ = aruco.detectMarkers(self.frame.image_gray[self.slice], ARUCO_DICT, parameters=ARUCO_PARAMS)
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, ARUCO_SIZE, CAMERA_INTRINSIC, None)
        # TODO: return relative position of aruco markers

    def crop_bounding_box(self, top_left, bottom_right):
        """
            top_left and bottom_right parameters are tuples.

        """

        # Define the colour (BGR) and thickness of the rectangle
        colour = (0, 255, 0)  # Green
        thickness = 2

        # Draw the bounding box on the image
        cv2.rectangle(self.frame.image_lab, top_left, bottom_right, colour, thickness)

        # Define an overlay slice to update the crop
        overlay_slice = np.s_[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        cropped_lab_image = self.frame.image_lab[overlay_slice]
       
        # Display the imagens with the bounding box
        cv2.imshow("Original Image", self.frame.image_lab)
        return (cropped_lab_image, np.count_nonzero(cropped_lab_image))

    @staticmethod
    def _slice_none(x): return 0 if x is None else x  # Cast None to 0 when handling slice start arithmetic

    @staticmethod
    def _compose_slices(s1: slice, s2: slice):
        """
        Compose slice objects such that for s3: arr[s1][s2] == arr[s3] for array arr.
        Does not handle negative indexing or slice steps > 1.
        """
        start = Crop._slice_none(s1.start) + Crop._slice_none(s2.start)
        print(start)
        stop = s1.stop if s2.stop is None else start + s2.stop
        if start == 0: start = None
        return slice(start, stop)

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
    filename = 'mcav_av_workshop/test/STOP.jpg'
    test_img = cv2.imread(filename, 1)
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    frame = Frame(test_img.shape[:2])
    frame.update_image(test_img)


    slice1 = (500, 200)
    slice2 = (1500, 1800)

    slice3 = (100,200)
    slice4 = (1300, 1700)
    test1 = Crop(frame, slice1)
    test2 = Crop(frame, slice3)

    aaa = test1.crop_bounding_box(slice1, slice2)
    bbb = test2.crop_bounding_box(slice3, slice4)
    
    cv2.imshow("Cropped Image1", aaa[0])
    cv2.imshow("Cropped Image2", bbb[0])

    # waits for user to press any key
    # (this is necessary to avoid Python kernel form crashing)
    cv2.waitKey(0)
    
    # closing all open windows
    cv2.destroyAllWindows()
        

    test_color_1 = highlight_color(aaa[0], RED, 30)
    test_color_2 = highlight_color(bbb[0], GREY, 30)

    #print(np.count_nonzero(test.img))
    #print(f"Pixel Count in bounding box: {pixel_count}")

    threshold = 20000

    #if pixel_count > threshold:
        #driving_tools Vehicle.stop()
    #    pass

    plt.imshow(test_color_1.img)
    plt.show()
    plt.imshow(test_color_2.img)
    plt.show()


