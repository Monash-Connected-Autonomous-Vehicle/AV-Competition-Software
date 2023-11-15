"""Runs a picamera using multiprocessing, provides a handle to a channel connection to receive camera frames as numpy arrays."""
from multiprocessing import Pipe, Process, connection, Event
from picamera2 import Picamera2
import multiprocessing as mp
import time
import threading
import sys
from PIL import Image


def drive_camera(channel: connection.Connection, is_done: threading.Event):
    with Picamera2 as picam2:
        camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)},
                                                        lores={"size": (640, 480)},
                                                            display="main")
        picam2.configure(camera_config)
        picam2.start()

        for i in range(50):
            if is_done.is_set():
                break
            array = picam2.capture_array("main")
            channel.send((time.time(), array))
            time.sleep(0.01)

def start_picamera() -> tuple[Process, connection.Connection, threading.Event]:
    """
    Requires no other processes utilising the picamera.
    Creates another process (multiprocessing) that runs the picamera to
    capture images as numpy arrays. The image data is sent over a Pipe; 
    to receive the data use listener.poll() to check for a message listener.recv()
    to get the data. Data is sent as a time-stampled tuple (send_time, image_array).

    ## TODO: Create an event to listen for when to close the picamera process.

    RESPONSIBILTIES:
        When done and closing:
            Must set is_done Event to release the camera from the process
            Then wait for camera sub-process to join()
            Then close the camera process 
        After this, everything should be released and can be garbage collected safely.

    Example:
        ## Listen for the most recent message over the pipe
        ## Then save the image
        for _ in range(100):
            received = False
            while listen.poll():
                sent_at, payload = listen.recv()
                received = True
            if received:
                print(f"FPS: {1/(time.time() - sent_at)}")
                # print(payload)
                image = Image.fromarray(payload, mode="RGB")
                image.save(f"bad_pictures/example_{time.time()}.jpg")
            time.sleep(0.1) ## A time delay is important to ensure the pipe lock is released for the sender to put messages
    """
    mp.set_start_method('fork')
    listen, shout = Pipe()
    is_done = Event()
    camera_process = Process(target=drive_camera, args=(shout, is_done,))
    camera_process.start()
    
    return camera_process, listen, is_done

if __name__ == '__main__':
    # mp.set_start_method('fork')
    # listen, shout = Pipe()
    
    # p = Process(target=drive_camera, args=(shout,))
    # p.start()
    
    # payload = None
    # for _ in range(100):
    #     received = False
    #     while listen.poll():
    #         sent_at, payload = listen.recv()
    #         received = True
    #     if received:

    #         print(f"FPS: {1/(time.time() - sent_at)}")
    #         # print(payload)
    #         image = Image.fromarray(payload, mode="RGB")
    #         image.save(f"bad_pictures/example_{time.time()}.jpg")

    #     time.sleep(0.1)
    # p.join()
    # p.close()
    # sys.exit()

    camera_process, visual_listener, is_done = start_picamera()
    payload = None
    for _ in range(20):
        received = False
        while visual_listener.poll():
            sent_at, payload = visual_listener.recv()
        if received:
            print("Received an image frame")
            image = Image.fromarray(payload, mode="RGB")
            image.save(f"bad_pictures/example_{time.time()}.jpg")
        time.sleep(0.1) # Delay to release lock on visual_listener for sending
    is_done.set()
    camera_process.join()
    camera_process.close()
    visual_listener.close()
    sys.exit()
