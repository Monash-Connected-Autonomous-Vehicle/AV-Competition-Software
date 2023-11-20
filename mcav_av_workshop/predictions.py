import os
import time
from dotenv import load_dotenv
from roboflow import Roboflow
from picamera2 import Picamera2
import cv2
from image_tools import Crop, Frame, highlight_color
import numpy as np
from motion import motion


RED = cv2.cvtColor(np.uint8([[[140, 15, 30]]]), cv2.COLOR_RGB2LAB)[0, 0, :]

def roboflow_model():
    load_dotenv()
    
    rf = Roboflow(api_key="{}".format(os.environ.get('ROBOFLOW_KEY')))  # Change to your API KEY
    project = rf.workspace().project("codedrive-traffic-lights")
    model = project.version(1, local='http://localhost:9001/').model
    
    return model

def init_camera():
    cam = Picamera2()
    capture_config = cam.create_still_configuration(main={"size": (1640, 1232)})
    cam.configure(capture_config)
    cam.start()
    time.sleep(1)
    
    return cam

def capture_image():
    cam_array = cam.capture_array("main")
    
    return cv2.cvtColor(cam_array, cv2.COLOR_BGRA2RGB)

def process_image(image, model):
    results = model.predict(image, confidence=50, overlap=50).json()
    draw_bounding_boxes(image, results['predictions'])

def draw_bounding_boxes(image, predictions):
    for prediction in predictions:
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

        frame = Frame(image.shape[:2])
        frame.update_image(image)

        slice1 = (x1, y1)
        slice2 = (x2, y2)

        test1 = Crop(frame, slice1)

        image_crop = test1.frame.image_lab[slice1[1]:slice2[1], slice1[0]:slice2[0]]
        check_threshold(image_crop, threshold=5, color=RED)
        
def check_threshold(image_crop, threshold, color):
    if image_crop is not None and image_crop.shape[0] > 0 and image_crop.shape[1] > 0:
        highlighted_image = highlight_color(image_crop, color, 40)
        
        # Check color threshold within the highlighted area
        if highlighted_image.check_color_threshold(threshold):
            print("Light is ON")
            motion.stop()
            time.sleep(0.5)
        else:
            print("Light is OFF")
            motion.drive_forward(5)

        # Display only the highlighted area within the bounding box
        cv2.imshow('Output', highlighted_image.img)
        

if __name__ == "__main__":
    motion.setup()
    
    cam = init_camera()
    model = roboflow_model()
    
    try:
        while True:
            test_img = capture_image(cam)
            process_image(test_img, model)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    finally:
        motion.destroy()
        cam.close()
        cv2.destroyAllWindows()
