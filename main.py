import RPi.GPIO as GPIO
import vehicle
import imageprocessor
import time
import sys

GPIO.setmode(GPIO.BCM)

shutdown_handlers = []
try:
    img_stream_thr = imageprocessor.ImageStreamThread(shutdown_handlers)
    img_processor = imageprocessor.ImageProcessor(img_stream_thr)

    time.sleep(1)

    vehicle = vehicle.Vehicle(img_processor, shutdown_handlers)
    vehicle.seek_and_destroy()

finally:
    print("Shutting down")
    for handler in shutdown_handlers:
        handler()


