import os
import time
from dotenv import load_dotenv
from roboflow import Roboflow
from picamera2 import Picamera2
import cv2

load_dotenv()

rf = Roboflow(api_key="{}".format(os.environ.get('ROBOFLOW_KEY')))  # Change to your API KEY
project = rf.workspace().project("codedrive-traffic-lights")
model = project.version(1, local='http://localhost:9001/').model

# Open a connection to the webcam (0 is usually the default camera)
cam = Picamera2()
capture_config = cam.create_still_configuration(main={"size": (1640, 1232)})
cam.configure(capture_config)
cam.start()
time.sleep(1)

# image_path = "./output_images/output_4.jpg"

# infer on a local image
# results = model.predict(image_path, confidence=36, overlap=50).json()

# Load the image
# image = cv2.imread(image_path, 1)

while cam.is_open:
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
    cv2.imshow('Webcam', img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cam.close()
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