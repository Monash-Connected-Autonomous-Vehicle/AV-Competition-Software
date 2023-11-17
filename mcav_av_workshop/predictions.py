import os
import time
from dotenv import load_dotenv
from roboflow import Roboflow
from picamera2 import Picamera2
import cv2
from image_tools import Crop, Frame, highlight_color
import numpy as np

load_dotenv()

RED = cv2.cvtColor(np.uint8([[[140, 15, 30]]]), cv2.COLOR_RGB2LAB)[0, 0, :]

rf = Roboflow(api_key="{}".format(os.environ.get('ROBOFLOW_KEY')))  # Change to your API KEY
project = rf.workspace().project("codedrive-traffic-lights")
model = project.version(1, local='http://localhost:9001/').model

# Open a connection to the webcam (0 is usually the default camera)
cam = Picamera2()
capture_config = cam.create_still_configuration(main={"size": (1640, 1232)})
cam.configure(capture_config)
cam.start()
time.sleep(1)

image_path = "./output_images/1700025778.0.jpg"

while True:
    cam_array = cam.capture_array("main")

    test_img = cv2.cvtColor(cam_array, cv2.COLOR_BGRA2RGB)
    # print(img.shape)
    # test_img = cv2.imread(cam_array, 1)

    # Infer on the captured frame
    results = model.predict(test_img, confidence=50, overlap=50).json()
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
        # label = f"Confidence: {confidence:.2%}"
        # cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=4)
        # cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        frame = Frame(test_img.shape[:2])
        frame.update_image(test_img)

        slice1 = (x1, y1)
        slice2 = (x2, y2)

        test1 = Crop(frame, slice1)
        # highlight red pixels in bounding box crop
        red_highlighted_image = highlight_color(test1.frame.image_lab[slice1[1]:slice2[1], slice1[0]:slice2[0]], RED,
                                                40)

        # Print information for debugging
        print("Threshold percentage:", red_highlighted_image.check_color_threshold(30))
        print("Percentage of red pixels:",
              (np.count_nonzero(red_highlighted_image.img) / red_highlighted_image.img.size) * 100)

        # Check color threshold within the highlighted area
        percentage = (np.count_nonzero(red_highlighted_image.img) / red_highlighted_image.img.size) * 100
        print("Calculated percentage:", percentage)

        if red_highlighted_image.check_color_threshold(5):
            print("Red light is ON")
            # stop()
        else:
            print("Red light is OFF")

        # Display only the highlighted area within the bounding box
        cv2.imshow('Output', red_highlighted_image.img)

    # Display the resulting frame
    # cv2.imshow('Webcam', img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
# cam.close()
cv2.destroyAllWindows()

# # visualize our prediction
# model.predict(image_path, confidence=40, overlap=80, stroke=2).save("prediction.jpg")

# # infer on an image hosted elsewhere
# # print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())

# Determining if traffic light is on or not
# for index, images in enumerate(os.listdir(folder_dir_2)):
#     image = cv2.imread(f"bound_box_img/{images}")
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     test_color_1 = highlight_color(image, RED, 30)
#     if test_color_1.check_color_threshold(50):
#         print(f"{images} Stops")
