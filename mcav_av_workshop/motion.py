import RPi.GPIO as GPIO
import time

PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23
BIN1 = 25
BIN2 = 24


def drive_forward(time_s):
    L_Motor.ChangeDutyCycle(40)
    R_Motor.ChangeDutyCycle(40)
    GPIO.output(AIN2, False)
    GPIO.output(AIN1, True)
    GPIO.output(BIN2, False)
    GPIO.output(BIN1, True)
    time.sleep(time_s)


def drive_backward(time_s):
    L_Motor.ChangeDutyCycle(40)
    R_Motor.ChangeDutyCycle(40)
    GPIO.output(AIN2, True)
    GPIO.output(AIN1, False)
    GPIO.output(BIN2, True)
    GPIO.output(BIN1, False)
    time.sleep(time_s)


def turn_left(time_s):
    L_Motor.ChangeDutyCycle(40)
    R_Motor.ChangeDutyCycle(40)
    GPIO.output(AIN2, True)
    GPIO.output(AIN1, False)
    GPIO.output(BIN2, False)
    GPIO.output(BIN1, True)
    time.sleep(time_s)


def turn_right(time_s):
    L_Motor.ChangeDutyCycle(40)
    R_Motor.ChangeDutyCycle(40)
    GPIO.output(AIN2, False)
    GPIO.output(AIN1, True)
    GPIO.output(BIN2, True)
    GPIO.output(BIN1, False)
    time.sleep(time_s)


def stop():
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)
    GPIO.output(AIN1, False)
    GPIO.output(BIN2, False)
    GPIO.output(BIN1, False)


def destroy():
    L_Motor.stop()
    R_Motor.stop()
    GPIO.cleanup()


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # set up GPIO Pins
    GPIO.setup(PWMA, GPIO.OUT)
    GPIO.setup(AIN1, GPIO.OUT)
    GPIO.setup(AIN2, GPIO.OUT)

    GPIO.setup(PWMB, GPIO.OUT)
    GPIO.setup(BIN1, GPIO.OUT)
    GPIO.setup(BIN2, GPIO.OUT)

    # Run the PWM
    global L_Motor
    global R_Motor
    L_Motor = GPIO.PWM(PWMA, 2000)
    L_Motor.start(0)

    R_Motor = GPIO.PWM(PWMB, 2000)
    R_Motor.start(0)


if __name__ == '__main__':
    setup()
    drive_forward(1)
    # drive_backward(5)
    # turn_right(1)
    destroy()
