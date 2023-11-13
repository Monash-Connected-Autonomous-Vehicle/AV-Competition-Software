from picamera2 import Picamera2, Preview
from dotenv import load_dotenv
from roboflow import Roboflow
import os
import time
import datetime

load_dotenv()


def run_model(image_file: float):
    """
    Runs trained Roboflow model hosted locally
    :param image_file: image file name without extension
    """
    rf = Roboflow(api_key='{}'.format(os.environ.get('ROBOFLOW_KEY')))
    project = rf.workspace().project('codedrive-traffic-lights')
    model = project.version(1).model
    prediction = model.predict('data/{}.jpg'.format(image_file), confidence=50, overlap=50).json()
    print(prediction)
    model.predict('data/{}.jpg'.format(image_file), confidence=50, overlap=50).save(
        'output/{}-model.jpg'.format(image_file))


if __name__ == '__main__':
    # Define the Camera Variable
    picam2 = Picamera2()

    # Initialise config
    preview_config = picam2.create_preview_configuration(main={"size": (1640, 1232)})
    # TODO: Look into resizing the captured image
    capture_config = picam2.create_still_configuration(main={"size": (1640, 1232)})
    # capture_config = picam2.create_still_configuration(main={ "size": (820, 616) })

    # Initiate the PiCamera
    picam2.configure(preview_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()

    while True:
        timestamp = datetime.datetime.now()
        unix_timestamp = time.mktime(timestamp.timetuple())
        time.sleep(5)

        picam2.switch_mode_and_capture_file(capture_config, file_output="data/{}.jpg".format(unix_timestamp))
        run_model(unix_timestamp)

    # # Request for the capturing of an image and convert it into array.
    # array = picam2.capture_array("main")
    # print(array.shape)

    # #rgba = cv2.cvtColor(array, cv2.COLOR_RGB2RGBA)
    # plt.imshow(array)
    # plt.show()
