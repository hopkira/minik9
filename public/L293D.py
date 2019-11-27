import RPi.GPIO as GPIO
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO - use sudo to run script")

GPIO.setmode(GPIO.BCM) # use Broadcom numbers not pin numbers

pin_list = [22,23,27,17] # pins for M1B, M1A, M2A, M2B - in that order
GPIO.setup(pin_list, GPIO.OUT) # set all pins for output mode

class Motor:
    '''Object that represents the each motor controlled by the L293D'''

    def __init__(self,name,pin_a,pin_b):
        '''Create a motor instance with a name and two GPIO pins

        Attributes
        ----------
        name : str
            The name of the motor
        pin_a : int
            Pin identified as MxA
        pin_b : int
            Pin identified as MxB

        Methods
        -------

        forward:
            Move motor forwards
        backward()
            Move motor backwards
        stop()
            Stop motor
        '''
        self.name = name
        self.pin_a = pin_a
        self.pin_b = pin_b
        print (str(name) + " motor instantiated")
        self.direction = 0

    def stop(self):
        GPIO.output(self.pin_a, GPIO.HIGH)
        GPIO.output(self.pin_b, GPIO.HIGH)

    def backward(self):
        GPIO.output(self.pin_a, GPIO.HIGH)
        GPIO.output(self.pin_b, GPIO.LOW)

    def forward(self):
        GPIO.output(self.pin_a, GPIO.LOW)
        GPIO.output(self.pin_b, GPIO.HIGH)

class Robot:
    '''Object that represents the movement of a simple two motor robot'''

    def __init__(self):
        '''Create robot instance with two (left and right) Motor objects

        Methods
        -------

        forward(dist):
            Move robot forwards for dist cms
        backward(dist):
            Move robot backwards for dist cms
        stop:
            Stop motor
        spin_right(turns):
            Spin robot turns in a clockwise direction
        spin_left(turns):
            Spin robot turns in an anti-clockwise direction
        '''
        self.left = Motor("left",pin_list[0],pin_list[1])
        self.right = Motor("right",pin_list[2],pin_list[3])
        self.speed = 0 # speed of robot in cms per second
        self.turn_speed = 0 # speed of robot in revolutions per second

    def stop(self,delay):
        time.sleep(delay)
        self.left.stop()
        self.right.stop()

    def forward(self,dist):
        self.left.forward()
        self.right.forward()
        self.stop(dist)

    def backward(self,dist):
        self.left.backward()
        self.right.backward()
        self.stop(dist)

    def spin_right(self,turns):
        self.left.backward()
        self.right.forward()
        self.stop(turns)

    def spin_left(self,turns):
        self.left.forward()
        self.right.backward()
        self.stop(turns)


