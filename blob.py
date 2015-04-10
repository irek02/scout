import io
import os.path
import time
import threading
import picamera
from PIL import Image

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []

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
                    
                    img = Image.open(self.stream)
                    data = list(img.getdata())
                    
                    cluster = []

                    f = open('/home/pi/scripts/tmp.txt', "w+")
                    for idx, item in enumerate(data):
                        if (sum(item) < 55):
                            #f.write(str(idx / 170) + ' ')
                            #data[idx] = tuple([240, 240, 240])
                            cluster.append(idx)

                    location = cluster[round((len(cluster) - 1) / 2)]
                    data[location] = tuple([250, 250, 250])

                    img.putdata(tuple(data))
                    img.save('img.jpg')
                     
                    #print(type(data[0][0]))




                    # Read the image and do some processing on it
                    #Image.open(self.stream)
                    done=True
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
    pool = [ImageProcessor() for i in range(4)]
    camera.resolution = (640, 480)
    camera.framerate = 30
    camera.start_preview()
    time.sleep(2)
    camera.capture_sequence(streams(), use_video_port=True)

# Shut down the processors in an orderly fashion
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
