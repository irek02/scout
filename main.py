import vehicle
import components
import time

resolution = (50, 40)

camera     = components.Camera(resolution)
target_loc = components.TargetLocator(resolution)
led        = components.Pin(15)
laser      = components.Pin(18)

time.sleep(1)

vehicle = vehicle.Vehicle(camera, target_loc, led, laser)

try:
    vehicle.seek_and_destroy()
except:
    vehicle.shutdown_procedure()


