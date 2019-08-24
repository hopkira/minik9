import RPi.GPIO as GPIO

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO - use sudo to run script")

GPIO.setmode(GPIO.BOARD)

pin_list = [17,22,23,27]
GPIO.setup(pin_list, GPIO.OUT)

left_motor = Motor("M1",22,23)
right_motor = Motor("M2",17,27)

GPIO.cleanup()

class Motor:
    def __init__(self,name,pin_a,pin_b)
        self.name = name 
        print (str(name) + " motor instantiated")
        self.direction = 0

    def one()
        GPIO.output(pin_a, GPIO.HIGH)
        GPIO.output(pin_b, GPIO.HIGH)

    def two()
        GPIO.output(pin_a, GPIO.HIGH)
        GPIO.output(pin_b, GPIO.LOW)

    def three()
        GPIO.output(pin_a, GPIO.LOW)
        GPIO.output(pin_b, GPIO.LOW)   

    def four()
        GPIO.output(pin_a, GPIO.LOW)
        GPIO.output(pin_b, GPIO.HIGH)   



