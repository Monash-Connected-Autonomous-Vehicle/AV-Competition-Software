from time import sleep
import RPi.GPIO as GPIO


class MotorChannel():
    """
    Control class for [MODEL] motor, via RPi GPIO pins
    
    Arguments
    ---------
    enable_pin : int
        GPIO pin number for enabling the motor
    forward_pin : int
        GPIO pin number for forward driving of the motor
    backward_pin : int
        GPIO pin number for forward driving of the motor
    """
    def __init__(self, enable_pin: int, forward_pin: int, backward_pin: int):
        # Setting up pins
        GPIO.setup(enable_pin, GPIO.OUT)       # Enable
        GPIO.setup(forward_pin, GPIO.OUT)      # Foward
        GPIO.setup(backward_pin, GPIO.OUT)     # Backward

        # Setting output of enable to software PWM
        self.pwm = GPIO.PWM(enable_pin, 5000)  # PWM on enable pin
        self.pwm.start(0)

        #GPIO pin numbers
        self.en = enable_pin
        self.fw = forward_pin
        self.bk = backward_pin
    
    def drive(self, duty_cycle: int, forward: bool):
        """
        Motor driving from duty cycle

        duty_cycle : int
            Duty cycle for motor driving PWM signal
        forward : bool
            Motor driving direction, True for forward and False for reverse
        """
        # Set direction pin high, other low
        GPIO.output(self.fw, forward)
        GPIO.output(self.bk, not forward)

        # Change enable to PWM
        self.pwm.ChangeDutyCycle(duty_cycle)

    def stop(self):
        """Stops motor operation"""
        self.pwm.ChangeDutyCycle(0)


class Vehicle():
    """
    Control class for differential drive vehicle

    Arguments
    ---------
    right_channel : MotorChannel
        Output specification for right motor
    left_channel : MotorChannel
        Output specification for left motor
    wheel_r : float
        Radius of driven/virtual wheel
    baseline : float
        Horizontal distance between left/right mean ground contacts
    """
    def __init__(self, right_channel: MotorChannel, left_channel: MotorChannel, wheel_r: float, baseline: float):
        self.motor_right = right_channel
        self.motor_left = left_channel
        self.wheel_r = wheel_r
        self.baseline = baseline
    
    def drive_linang(self, lin: float, ang: float):
        """
        Sets the linear and angular velocity of the vehicle

        Arguments
        ---------
        lin : float
            Linear velocity of vehicle in meters per second
        ang : float
            Angular velocity of vehicle in radians per second
        """
        # TODO: Math for driving motors from linear/angular velocity
        pass

    def stop(self):
        """Stops vehicle driving"""
        self.motor_right.stop()
        self.motor_left.stop()
