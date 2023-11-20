import os
import time

import cv2
import numpy as np
from typing import Any, Callable
from dotenv import load_dotenv
from roboflow import Roboflow
from picamera2 import Picamera2
from mcav_av_workshop import motion
from mcav_av_workshop.camera.image_tools import Crop, Frame, highlight_color

load_dotenv()


def get_model():
    """
    Retrieves Roboflow model
    """
    rf = Roboflow(api_key="{}".format(os.environ.get('ROBOFLOW_KEY')))  # Load key from .env
    project = rf.workspace().project("codedrive-traffic-lights")
    model = project.version(1, local='http://localhost:9001/').model
    return model


def init_camera():
    """
    Opens a connection to the webcam (0 is usually the default camera)
    """
    cam = Picamera2()
    capture_config = cam.create_still_configuration(main={"size": (1640, 1232)})
    video_config = cam.create_video_configuration(main={"size": (1920, 1080)},
                                                  lores={"size": (640, 480)},
                                                  controls={"FrameRate": 60},
                                                  buffer_count=6)
    cam.configure(capture_config)
    cam.start()
    time.sleep(1)
    return cam


def detect_colour(image, colour, colour_variance, threshold, drive_fn: Callable):
    if image is not None and image.shape[0] > 0 and image.shape[1] > 0:
        highlighted_image = highlight_color(image, colour, colour_variance)

        # Check color threshold within the highlighted area
        percentage = (np.count_nonzero(highlighted_image.img) / highlighted_image.img.size) * 100
        print("Percentage of colour detected: {}%".format(percentage))

        if highlighted_image.check_color_threshold(threshold):
            print("Red light is ON")
            motion.stop()
            time.sleep(0.5)
        else:
            print("Red light is OFF")
            drive_fn()

        # Display only the highlighted area within the bounding box
        cv2.imshow('Colour Detection', highlighted_image.img)


def preview_obj_detection():
    model = get_model()
    cam = init_camera()

    while True:
        cam_array = cam.capture_array("main")

        img = cv2.cvtColor(cam_array, cv2.COLOR_BGRA2RGB)
        print(img.shape)

        # Infer on the captured frame
        results = model.predict(img, confidence=50, overlap=50).json()
        print(results)

        # Draw bounding boxes on the image
        for prediction in results['predictions']:
            x = int(prediction['x'])
            y = int(prediction['y'])
            width = int(prediction['width'])
            height = int(prediction['height'])
            confidence = prediction['confidence']

            # Calculate coordinates of the bounding box
            x1 = int(x - width / 2)
            x2 = int(x + width / 2)
            y1 = int(y - height / 2)
            y2 = int(y + height / 2)

            # Draw the bounding box
            label = f"Confidence: {confidence:.2%}"
            cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=4)
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

        # Display the resulting frame
        cv2.imshow('Object Detection Preview', img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture and remove all windows
    cam.close()
    cv2.destroyAllWindows()


def drive_with_obj_colour_detection(colour: Any, colour_variance: Any, threshold: Any, drive_fn: Callable):
    """
    Perform object detection in conjunction with colour filtering
    and provide a callback function to execute drive commands while NO object is detected
    Parameters
    ----------
    drive_fn
    colour
    colour_variance
    threshold: percentage of matching colour in bounding box to trigger stop

    Returns
    -------

    """
    motion.setup()
    model = get_model()
    cam = init_camera()

    while True:
        cam_array = cam.capture_array("main")
        test_img = cv2.cvtColor(cam_array, cv2.COLOR_BGRA2RGB)

        # Predict on the captured frame
        results = model.predict(test_img, confidence=50, overlap=50).json()
        print(results)

        for prediction in results['predictions']:
            # Retrieve prediction details
            x = int(prediction['x'])
            y = int(prediction['y'])
            width = int(prediction['width'])
            height = int(prediction['height'])
            confidence = prediction['confidence']

            # Calculate coordinates of the bounding box
            x1 = int(x - width / 2)
            x2 = int(x + width / 2)
            y1 = int(y - height / 2)
            y2 = int(y + height / 2)

            # Create a frame and crop to slice coordinates
            frame = Frame(test_img.shape[:2])
            frame.update_image(test_img)
            slice1 = (x1, y1)
            slice2 = (x2, y2)
            test1 = Crop(frame, slice1)

            image_crop = test1.frame.image_lab[slice1[1]:slice2[1], slice1[0]:slice2[0]]
            detect_colour(image_crop, colour, colour_variance, threshold, drive_fn)

        # Drive if there is no detection
        drive_fn()

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    motion.destroy()
    cam.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    preview_obj_detection()


    def drive():
        motion.drive_forward(5)
