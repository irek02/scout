import io
import os.path
import RPi.GPIO as GPIO
import time
import threading
import picamera
from PIL import Image

GPIO.setmode(GPIO.BCM)  
# set up GPIO output channel  
GPIO.setup(4, GPIO.OUT)
GPIO.output(4,GPIO.LOW)

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []

res_w = 30
res_h = 20
x_range = range(round(res_w / 2 - 2), round(res_w / 2 + 2))
y_range = range(round(res_h / 2 - 1), round(res_h / 2 + 1))
grid = []
i = 0
for y in range(1, res_h):
    for x in range(1, res_w):
        grid.insert(i, (x, y))
        i = i + 1


class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # This method runs in a separate thread
        global done
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)

                    GPIO.output(4,GPIO.LOW)
                    
                    img = Image.open(self.stream)
                    pixels = img.load()
                    
                    x_cluster = []
                    y_cluster = []
                    for x in range(1, res_w):
                        for y in range(1, res_h):
                            if (sum(pixels[x,y]) < 55):
                                x_cluster.append(x)
                                y_cluster.append(y)

                    if (len(x_cluster) and len(y_cluster)):
                        x_center = round(sum(x_cluster)/len(x_cluster))
                        y_center = round(sum(y_cluster)/len(y_cluster))
                        if (y_center in y_range):
                            if (x_center in x_range):
                                #print('centered!')
                                GPIO.output(4,GPIO.HIGH)
                            else:
                                if (x_center < x_range[0]):
                                    print("fly left")
                                elif (x_center > x_range[len(x_range) - 1]):
                                    print("fly right")
                        else:
                            if (y_center < y_range[0]):
                                print("fly up")
                            elif (y_center > y_range[len(y_range) - 1]):
                                print("fly down")

                           
              

                    #f = open('/home/pi/scripts/tmp.txt', "w+")
                    #f.write(str(idx / 170) + ' ')
                      
                    #done=True
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)

def streams():
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # When the pool is starved, wait a while for it to refill
            time.sleep(0.1)






with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range(1)]
    camera.resolution = (res_w, res_h)
    camera.framerate = 10
    camera.start_preview()
    time.sleep(2)
    camera.capture_sequence(streams(), use_video_port=True)

# Shut down the processors in an orderly fashion
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
