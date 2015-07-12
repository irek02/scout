import vehicle
import components
import time
import picamera

from components.targetlocator import TargetLocator
from components.camera import Camera
from components.gpiopin import Pin

resolution = (50, 40)

picam = picamera.PiCamera()
picam.resolution = resolution

camera     = components.Camera(picam)
target_loc = components.TargetLocator(resolution)
led        = components.Pin(15)
laser      = components.Pin(18)

time.sleep(1)

vehicle = vehicle.Vehicle(camera, target_loc, led, laser)

try:
    vehicle.seek_and_destroy()
except:
    vehicle.shutdown_procedure()
