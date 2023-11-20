"""
This is where you will write all your code!~
"""

# Here we are importing the 'predict' and 'motion' modules from the 'mcav_av_workshop' package
from mcav_av_workshop import predict, motion, colours


def main():
    # predict.preview_obj_detection()
    predict.obj_detection_with_motor(colours.RED, 40, 1, drive_callback)


def drive():
    motion.setup()
    # Perform driving commands here

    motion.destroy()


def drive_callback():
    # Perform driving commands for when traffic light is not detected
    # No need to setup or destroy here
    pass


if __name__ == '__main__':
    # Run functions above here, e.g.:
    main()
