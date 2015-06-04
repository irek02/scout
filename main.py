import io
import os.path
import RPi.GPIO as GPIO
import time
import picamera
import vehicle
from PIL import Image

with picamera.PiCamera() as camera:
	camera.resolution = (res_w, res_h)
	camera.framerate = 10
	camera.start_preview()
	time.sleep(2)

	img_processor = ImageProcessor(camera)
	vehicle = vehicle.Vehicle(img_processor)
	vehicle.seek_and_destoy()


class ImageProcessor:
	def __init__(self, camera):
		self.stream = io.BytesIO()
		self.target_loc = None
        camera.capture_sequence(stream_generator(), use_video_port=True)

	def stream_generator(self):
	    while True:
	        stream.truncate()
	        stream.seek(0)
	        yield stream
	        target_loc = calc_target_loc()

	def get_target_loc(self):
		return target_loc

	def getPixels(self):
		return Image.open(self.stream).load()

	def calc_target_loc(self):
	 
	    pixels = getPixels()
	    
	    x_cluster = []
	    y_cluster = []
	    for x in range(1, res_w):
	        for y in range(1, res_h):
	            if (sum(pixels[x,y]) < 55):
	                x_cluster.append(x)
	                y_cluster.append(y)

	    if (len(x_cluster) == 0 or len(y_cluster) == 0):
	        return
	    
	    x_center = round(sum(x_cluster)/len(x_cluster))
	    y_center = round(sum(y_cluster)/len(y_cluster))

	    if (y_center not in y_range):
	        GPIO.output(pin_led, GPIO.LOW)
	        on_target = 0
	        if (y_center < y_range[0]):
	            return 'up'
	        else:
	            return 'down'

	    if (x_center not in x_range):
	        GPIO.output(pin_led, GPIO.LOW)
	        on_target = 0
	        if (x_center < x_range[0]):
	            return 'left'
	        else:
	            return 'right'
	    
	    return 'center'


