"""
Image related operations for the AV workshop.
"""

import numpy as np
import cv2
from cv2 import aruco

from mcav_av_workshop import config


class Frame:
    """
    """
    def __init__(self, resolution) -> None:
        self.resolution = resolution
        self.camera_intrisic = config.CAMERA_INTRINSIC
        self.camera_distortion = config.CAMERA_DISTORTION

        self.rect_mat, self.roi = cv2.getOptimalNewCameraMatrix(config.CAMERA_INTRINSIC, config.CAMERA_DISTORTION, 
                                                                resolution, 1, resolution)
        self.mapx, self.mapy = cv2.initUndistortRectifyMap(config.CAMERA_INTRINSIC, config.CAMERA_DISTORTION, 
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
        assert isinstance(overlay_slice, np.s_)
        return Crop(self.frame, np.s_[Crop._compose_slices(self.slice[0], overlay_slice[0]), 
                                      Crop._compose_slices(self.slice[1], overlay_slice[1])])
        

    def aruco_pos(self):
        corners, ids, _ = aruco.detectMarkers(self.frame.image_gray[self.slice], config.ARUCO_DICT, parameters=config.ARUCO_PARAMS)
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, config.ARUCO_SIZE, config.CAMERA_INTRINSIC, None)
        # TODO: return relative position of aruco markers


    @staticmethod
    def _slice_none(x): 0 if x in None else x  # Cast None to 0 when handling slice start arithmetic

    @staticmethod
    def _compose_slices(s1: slice, s2: slice):
        """
        Compose slice objects such that for s3: arr[s1][s2] == arr[s3] for array arr.
        Does not handle negative indexing or slice steps > 1.
        """
        start = Crop._slice_none(s1.start) + Crop._slice_none(s1.start)
        stop = s1.stop if s2.stop is None else start + s2.stop
        if start == 0: start = None
        return slice(start, stop)