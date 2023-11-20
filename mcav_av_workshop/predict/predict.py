import os
import time

import cv2
import numpy as np
from typing import Any, Callable
from dotenv import load_dotenv
from roboflow import Roboflow
from picamera2 import Picamera2
from mcav_av_workshop.motion import motion
from mcav_av_workshop.camera.image_tools import Crop, Frame, highlight_color, RED

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
    cam.configure(capture_config)
    cam.start()
    time.sleep(1)
    return cam


def preview_obj_detection(cam: Any, model: Any):
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


def obj_detection_with_motor(cam: Any, model: Any, drive_fn: Callable):
    """
    Perform object detection and provide a callback function to
    execute drive commands while NO object is detected
    Parameters
    ----------
    drive_fn
    cam
    model

    Returns
    -------

    """
    motion.setup()

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
            print(image_crop.shape)
            # highlight red pixels in bounding box crop
            if image_crop is not None and image_crop.shape[0] > 0 and image_crop.shape[1] > 0:
                red_highlighted_image = highlight_color(image_crop, RED, 40)

                # Print information for debugging
                print("Threshold percentage:", red_highlighted_image.check_color_threshold(30))
                print("Percentage of red pixels:",
                      (np.count_nonzero(red_highlighted_image.img) / red_highlighted_image.img.size) * 100)

                # Check color threshold within the highlighted area
                percentage = (np.count_nonzero(red_highlighted_image.img) / red_highlighted_image.img.size) * 100
                print("Calculated percentage:", percentage)

                if red_highlighted_image.check_color_threshold(5):
                    print("Red light is ON")
                    motion.stop()
                    time.sleep(0.5)
                else:
                    print("Red light is OFF")
                    motion.drive_forward(5)

                # Display only the highlighted area within the bounding box
                cv2.imshow('Output', red_highlighted_image.img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    motion.destroy()
    cam.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    model = get_model()
    cam = init_camera()
    preview_obj_detection(cam, model)
