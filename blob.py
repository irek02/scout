import io
import os.path
import RPi.GPIO as GPIO
import time
import picamera
from PIL import Image


GPIO.setmode(GPIO.BCM)

pin = 18
pin_led = 15

GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin,GPIO.LOW)

GPIO.setup(pin_led, GPIO.OUT)
GPIO.output(pin_led,GPIO.LOW)


# Create a pool of image processors.
done = False

# Set the resolution and target boundaries.
res_w = 50
res_h = 40
x_range = range(round(res_w / 2 - 1), round(res_w / 2 + 1))
y_range = range(round(res_h / 2 - 1), round(res_h / 2 + 1))

# Tracking target lock vars.
on_target = 0
target_lock_time = 2

def imageprocessor(stream):
    global done
    global on_target
 
    img = Image.open(stream)
    pixels = img.load()
    
    x_cluster = []
    y_cluster = []
    for x in range(1, res_w):
        for y in range(1, res_h):
            if (sum(pixels[x,y]) < 55):
                x_cluster.append(x)
                y_cluster.append(y)

    if (len(x_cluster) == 0):
        return False

    if (len(y_cluster) == 0):
        return False
    
    x_center = round(sum(x_cluster)/len(x_cluster))
    y_center = round(sum(y_cluster)/len(y_cluster))

    if (y_center not in y_range):
        GPIO.output(pin_led, GPIO.LOW)
        on_target = 0
        if (y_center < y_range[0]):
            print("fly up")
        else:
            print("fly down")
        return False

    if (x_center not in x_range):
        GPIO.output(pin_led, GPIO.LOW)
        on_target = 0
        if (x_center < x_range[0]):
            print("fly left")
        else:
            print("fly right")
        return False
    
    # At this point the target is in the fire range.
    # Ensure the target is locked and open fire.
    print('centered!')
    if (on_target == 0):
        on_target = time.time()
        GPIO.output(pin_led, GPIO.HIGH)
    elif (time.time() - on_target > target_lock_time):
        engage_target()
        on_target = 0
        print('Target engaged.')
        done = True
        return True

def engage_target():
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(pin,GPIO.LOW)
    GPIO.output(pin_led, GPIO.LOW)

def stream_generator():
    stream = io.BytesIO()
    while not done:
        stream.truncate()
        stream.seek(0)
        yield stream
        imageprocessor(stream)
        

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (res_w, res_h)
        camera.framerate = 10
        camera.start_preview()
        time.sleep(2)
        camera.capture_sequence(stream_generator(), use_video_port=True)

except:
    # In case if something went wrong, shutdown the laser.
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin_led, GPIO.LOW)

GPIO.cleanup()
