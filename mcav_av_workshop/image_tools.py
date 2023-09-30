"""
Image related operations for the AV workshop.
"""

import numpy as np
import cv2
from cv2 import aruco
from matplotlib import pyplot as plt
    
from config import*


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
    def __init__(self, frame, slice, image) -> None:
        self.frame = frame
        self.slice = slice
        self.image = image

    
    def __getitem__(self, overlay_slice):
        print(overlay_slice)
        return Crop(self.frame, np.s_[Crop._compose_slices(self.slice[0], overlay_slice[0]), 
                                      Crop._compose_slices(self.slice[1], overlay_slice[1])], self.image)
        

    def aruco_pos(self):
        corners, ids, _ = aruco.detectMarkers(self.frame.image_gray[self.slice], ARUCO_DICT, parameters=ARUCO_PARAMS)
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, ARUCO_SIZE, CAMERA_INTRINSIC, None)
        # TODO: return relative position of aruco markers

    def crop_bounding_box(img, top_left, bottom_right):
        """
            top_left and bottom_right parameters are tuples.

        """
        # Convert image to Lab format colour
        img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

        frame = Frame(img.shape[:2])
        frame.update_image(img)

        # Define the colour (BGR) and thickness of the rectangle
        colour = (0, 255, 0)  # Green
        thickness = 2

        # Draw the bounding box on the image
        cv2.rectangle(frame.image_lab, top_left, bottom_right, colour, thickness)

        # Crop just the bounding box
        crop = Crop(frame, np.s_[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]], test_img)

        # Define an overlay slice to update the crop
        overlay_slice = np.s_[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]

        cropped_lab_image = crop.frame.image_lab[overlay_slice]

        # Adjust the windows so that they fit within screen :)
        cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Cropped Image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Cropped Image', top_left[0], top_left[1])
        
        # Display the images with the bounding box
        cv2.imshow("Original Image", frame.image_lab)
        cv2.imshow("Cropped Image", cropped_lab_image)
        print("Total Pixels in bounding box:", np.count_nonzero(cropped_lab_image)) # for testing
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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
    
if __name__ == '__main__':
    """
    Junk testing code can go here, this file should never be called directly in normal operation
    """
    test_img = cv2.imread('mcav_av_workshop/STOP.jpg')
    Crop.crop_bounding_box(test_img, (500, 500), (1500, 1500))
    
    # plt.imshow(test.img)
    # plt.show()