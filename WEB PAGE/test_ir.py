import RPi.GPIO as GPIO
import time

# declare the sensor and led pin
sensor_pin = 31

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor_pin, GPIO.IN)

try:
    while True:
        if GPIO.input(sensor_pin):
            print("mark detected!")
        else:
            # If an object is detected
            print("no mark!")
except KeyboardInterrupt:
    GPIO.cleanup()
