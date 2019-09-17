import RPi.GPIO as GPIO
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO - use sudo to run script")

GPIO.setmode(GPIO.BCM)

pin_list = [5,6,13,19,26,12,16,20,21]
GPIO.setup(pin_list, GPIO.OUT)

for pin in pin_list:
   GPIO.output(pin,GPIO.HIGH)
   print(pin)
   time.sleep(2)
   GPIO.output(pin,GPIO.LOW)

GPIO.cleanup()

