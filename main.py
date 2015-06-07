import os.path
import RPi.GPIO as GPIO
import time
import picamera
import vehicle
import imageprocessor


GPIO.setmode(GPIO.BCM)

img_processor = imageprocessor.ImageProcessorThread()

vehicle = vehicle.Vehicle(img_processor)

vehicle.seek_and_destroy()

# Shutdown the laser.
#GPIO.output(pin, GPIO.LOW)
#GPIO.output(pin_led, GPIO.LOW)

GPIO.cleanup()