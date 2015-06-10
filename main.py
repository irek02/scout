import RPi.GPIO as GPIO
import vehicle
import imageprocessor
import time

GPIO.setmode(GPIO.BCM)

shutdown_handlers = []

img_stream_thr = imageprocessor.ImageStreamThread(shutdown_handlers)
img_processor = imageprocessor.ImageProcessor(img_stream_thr)

time.sleep(1)

vehicle = vehicle.Vehicle(img_processor)
vehicle.seek_and_destroy()


for handler in shutdown_handlers:
    handler()


# Shutdown the laser.
GPIO.output(pin, GPIO.LOW)
GPIO.output(pin_led, GPIO.LOW)

GPIO.cleanup()

