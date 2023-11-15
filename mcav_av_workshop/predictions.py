from roboflow import Roboflow
import cv2

rf = Roboflow(api_key="YOUR_API_KEY")   # Change to your API KEY
project = rf.workspace().project("codedrive-traffic-lights")
model = project.version(1).model

# Open a connection to the webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

#image_path = "./output_images/output_4.jpg"

# infer on a local image
#results = model.predict(image_path, confidence=36, overlap=50).json()

# Load the image
#image = cv2.imread(image_path, 1)

while True:
    ret, frame = cap.read()
    
    # Infer on the captured frame
    results = model.predict(frame, confidence=36, overlap=50).json()
    
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
        cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=4)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('Webcam', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()

# # visualize our prediction
# model.predict(image_path, confidence=40, overlap=80, stroke=2).save("prediction.jpg")

# # infer on an image hosted elsewhere
# # print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())