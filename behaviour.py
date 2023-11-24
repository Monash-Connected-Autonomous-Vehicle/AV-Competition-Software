"""
This is where you will write all your code!~
"""

# Here we are importing the 'predict' and 'motion' modules from the 'mcav_av_workshop' package
from mcav_av_workshop import colours, motion, predict


def main():
    """
    Test out object detection commands here :D
    """
    predict.preview_obj_detection()


def drive():
    """
    Test out driving commands here :)
    """
    motion.setup()
    # Perform driving commands here

    motion.destroy()


def drive_callback():
    """
    Perform these driving commands while traffic light is NOT detected

    - There is no need to call motion.setup() or motion.destroy() here

    ——————————————————————————————————————————————————————————————
    Please use short driving command (<1 second) as these commands
    will be called in a loop
    ——————————————————————————————————————————————————————————————
    """

    pass


if __name__ == '__main__':
    # Run functions above here, e.g.:
    main()
