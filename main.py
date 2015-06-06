import os.path
import RPi.GPIO as GPIO
import time
import picamera
import vehicle
import imageprocessor


GPIO.setmode(GPIO.BCM)

pin = 18
pin_led = 15

GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin,GPIO.LOW)

GPIO.setup(pin_led, GPIO.OUT)
GPIO.output(pin_led,GPIO.LOW)

# Set the resolution and target boundaries.
res_w = 50
res_h = 40

with picamera.PiCamera() as camera:
	camera.resolution = (res_w, res_h)
	camera.framerate = 10
	camera.start_preview()
	#time.sleep(2)

	img_processor = imageprocessor.ImageProcessor(camera)
	print("hey2")
	vehicle = vehicle.Vehicle(img_processor)
	print("hey3")
	vehicle.seek_and_destoy()

# Shutdown the laser.
GPIO.output(pin, GPIO.LOW)
GPIO.output(pin_led, GPIO.LOW)

GPIO.cleanup()

