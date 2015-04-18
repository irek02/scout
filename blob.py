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

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []


class ImageProcessor(threading.Thread):
    def __init__(self, grid, res_w, res_h, x_range, y_range):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.grid = grid
        self.res_w = res_w
        self.res_h = res_h
        self.x_range = x_range
        self.y_range = y_range
        self.start()

    def centercrop(self):
        return img.crop(self.box)

    def run(self):
        # This method runs in a separate thread
        global done
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)
                    
                    img = Image.open(self.stream)
                    pixels = img.load()
                    
                    x_cluster = []
                    y_cluster = []
                    for x in range(1, self.res_w):
                        for y in range(1, self.res_h):
                            if (sum(pixels[x,y]) < 55):
                                x_cluster.append(x)
                                y_cluster.append(y)

                    if (len(x_cluster) and len(y_cluster)):
                        x_center = round(sum(x_cluster)/len(x_cluster))
                        y_center = round(sum(y_cluster)/len(y_cluster))
                        if (y_center in self.y_range):
                            if (x_center in self.x_range):
                                print('centered!')
                            else:
                                if (x_center < self.x_range[0]):
                                    print("fly left")
                                elif (x_center > self.x_range[len(self.x_range) - 1]):
                                    print("fly right")
                        else:
                            if (y_center < self.y_range[0]):
                                print("fly up")
                            elif (y_center > self.y_range[len(self.y_range) - 1]):
                                print("fly down")


                        

                        '''
                            GPIO.output(4,GPIO.HIGH)
                        else:
                            GPIO.output(4,GPIO.LOW)
                        '''     
                    #with pixels[sum(x_cluster)/len(x_cluster), sum(y_cluster)/len(y_cluster)] as pixel:
                     #   print(pixel)
                           
                    ''' 
                    if (len(detected)):
                        x, y = detected
                        if (x in self.x_range and y in self.y_range):
                            print(detected)
                        else:
                            print(' ')
                    else:
                        print(' ')
'''


                    '''
                    data = list(img.getdata())
                    
                    cluster = []

                    #f = open('/home/pi/scripts/tmp.txt', "w+")
                    
                    for idx, item in enumerate(data):
                        if (sum(item) < 35):
                            #f.write(str(idx / 170) + ' ')
                            #data[idx] = tuple([240, 240, 240])
                            cluster.append(idx)
                    
                    if (len(cluster) > 10):
                        location = cluster[round((len(cluster) - 1) / 2)]
                        x, y = self.grid[location]

                        if (x < 80):
                            data[location] = tuple([250, 250, 250])
                            img.putdata(tuple(data))
                            img.save('img.jpg')
                            done=True

                        #print(location)
                        print(str(location) + ': ' + str(self.grid[location]))
                        '''
                        #if (x in self.x_range):
                        #    GPIO.output(4,GPIO.HIGH)
                        #    print(str(x))
                        #else:
                        #    GPIO.output(4,GPIO.LOW)



                        #data[location] = tuple([250, 250, 250])

                        #for x in self.center_pxls:
                            #data[x] = tuple([250, 0, 0])

                        #img.putdata(tuple(data))
                        #img.save('img.jpg')
                        #done=True

                     
                    #print(type(data[0][0]))

                    


                    # Read the image and do some processing on it
                    #Image.open(self.stream)
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

print(str(x_range))
print(str(y_range))

def get_box(res_w, res_h):

    w_center = res_w / 2
    h_center = res_h / 2

    tolerance_factor = 0.1

    left = int(w_center - w_tolerance)
    upper = int(h_center - h_tolerance)
    right = int(w_center + w_tolerance)
    lower = int(h_center + h_tolerance)

    return (left, upper, right, lower)



with picamera.PiCamera() as camera:
    pool = [ImageProcessor(grid, res_w, res_h, x_range, y_range) for i in range(1)]
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
