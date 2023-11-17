"""Runs a picamera using multiprocessing, provides a handle to a channel connection to receive camera frames as numpy arrays."""
from multiprocessing import Pipe, Process, connection, Event
from picamera2 import Picamera2
import multiprocessing as mp
import time
import threading
import sys


def drive_camera(channel: connection.Connection, is_done: threading.Event):
    """The process function for producing camera frames
    TODO: Consider using a Queue for non-blocking synchronisation, stuck on take 1 push 1 might be capping speed
    """
    with Picamera2() as picam2:
        camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)},
                                                        lores={"size": (640, 480)},
                                                            display="main")
        picam2.configure(camera_config)
        picam2.set_controls({"FrameRate": 40}) # Manually increase beyond 15 fps default
        picam2.start()

        while True:
            array = picam2.capture_array("main")
            if channel.poll() is False:
                channel.send((time.time(), array))
            if is_done.is_set():
                break
            # print("captured")
            time.sleep(0.01) # Delay to release lock on channel to allow receiving

def start_picamera() -> tuple[Process, connection.Connection, threading.Event]:
    """
    Requires no other processes utilising the picamera.
    Creates another process (multiprocessing) that runs the picamera to
    capture images as numpy arrays. The image data is sent over a Pipe; 
    to receive the data use listener.poll() to check for a message listener.recv()
    to get the data. Data is sent as a time-stampled tuple (send_time, image_array).

    RECOMMENDED USE: 
        Use the PicameraManager class as a context using with PicameraManager() as listener:
        This wraps the setup and burndown of the subprocess with the context avoiding process leaks.

    RESPONSIBILTIES:
        When done and closing:
            Must set is_done Event to release the camera from the process
            Then wait for camera sub-process to join()
            Then close the camera process 
        After this, everything should be released and can be garbage collected safely.

    COMMON BUGS:
        Camera failed to initialise -> The camera is already locked by a process

    Example:
    with PicameraManager() as visual_listener:
        payload = None
        loop_time = time.time()
        delays = list()
        MAX_DELAY = 0.2 # Try to skip images more than MAX_DELAY seconds old
        for _ in range(1000):
            received = False
            while visual_listener.poll():
                sent_at, payload = visual_listener.recv()
                received = True
                if sent_at - loop_time < MAX_DELAY:
                    break
            if received:
                delay = time.time() - sent_at
                delays.append(delay)
                # print(f"Received an image frame, delay: {delay}, FPS: {1/delay}")
                # image = Image.fromarray(payload, mode="RGB")
                # image.save(f"bad_pictures/example_{time.time()}.jpg")
            time.sleep(0.05) # Delay to release lock on visual_listener for sending
            loop_time = time.time()
    print(f"Average delay: {sum(delays)/len(delays)}; Average FPS: {1/sum(delays)*len(delays)}"
    """
    mp.set_start_method('fork')
    listen, shout = Pipe()
    is_done = Event()
    camera_process = Process(target=drive_camera, args=(shout, is_done,))
    camera_process.start()
    
    return camera_process, listen, is_done

class PicameraManager():
    """
    Wrapper class for Picamera to use multiprocessing for picture capture.
    Usable with the context manager pattern 
    """

    def __init__(self) -> None:
        self.camera_process, self.listener, self.is_done = start_picamera()
        
    def start(self) -> bool:
        if not self.camera_process.is_alive():
            self.camera_process.start()
            return True
        return False
    
    def finish(self) -> bool:
        """Attempt to join the camera process and close pipes, signal the camera process to halt with is_done Event
        Returns if the process was successfully joined
        """
        exit_code = None
        try:
            self.is_done.set()
            if self.listener.poll():
                self.listener.recv() # Remove block for sender to allow exit condition
            self.camera_process.join(timeout=15)
            exit_code = self.camera_process.exitcode
            self.camera_process.close()
            self.listener.close()
        finally:
            return exit_code is not None 
            
    def __enter__(self):
        self.start()
        return self.listener
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()

if __name__ == '__main__':
    """Testing just using capture_array on raw output resulted in a max fps of around 14 to 15
    Using the context manager keeps the buildup and burndown steps for the picamera subprocess managed
    """

    with PicameraManager() as visual_listener:
        payload = None
        loop_time = time.time()
        delays = list()
        MAX_DELAY = 0.2 # Try to skip images more than MAX_DELAY seconds old
        for _ in range(1000):
            received = False
            while visual_listener.poll():
                sent_at, payload = visual_listener.recv()
                received = True
                if sent_at - loop_time < MAX_DELAY:
                    break

            if received:
                delay = time.time() - sent_at
                delays.append(delay)
                # print(f"Received an image frame, delay: {delay}, FPS: {1/delay}")
                # image = Image.fromarray(payload, mode="RGB")
                # image.save(f"bad_pictures/example_{time.time()}.jpg")
            time.sleep(0.05) # Delay to release lock on visual_listener for sending
            loop_time = time.time()
    print(f"Average delay: {sum(delays)/len(delays)}; Average FPS: {1/sum(delays)*len(delays)}"
