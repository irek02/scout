import io
from PIL import Image
import threading
import picamera
import time

class ImageProcessorThread(threading.Thread):
    def __init__(self):
        super(ImageProcessorThread, self).__init__()

        self.terminated = False

        self.res_w, self.res_h = (50, 40)

        self.cam = picamera.PiCamera()
        self.cam.resolution = (self.res_w, self.res_h)
        self.cam.framerate = 10

        self.target_loc = None        
        self.x_range = range(round(self.res_w / 2 - 1), round(self.res_w / 2 + 1))
        self.y_range = range(round(self.res_h / 2 - 1), round(self.res_h / 2 + 1))
        
        self.start()

    def run(self):
        stream = io.BytesIO()
        while not self.terminated:
            self.cam.capture(stream, format='jpeg', use_video_port=True)
            pixels = Image.open(stream).load()
            self.target_loc = self.calc_target_loc(pixels)
            stream.truncate()
            stream.seek(0)

    def get_target_loc(self):
        print(self.target_loc)
        return self.target_loc

    def getPixels(self):
        return Image.open(self.stream).load()

    def calc_target_loc(self, pixels):
        x_cluster = []
        y_cluster = []
        for x in range(1, self.res_w):
            for y in range(1, self.res_h):
                if (sum(pixels[x,y]) < 55):
                    x_cluster.append(x)
                    y_cluster.append(y)

        if (len(x_cluster) == 0 or len(y_cluster) == 0):
            return
        
        x_center = round(sum(x_cluster)/len(x_cluster))
        y_center = round(sum(y_cluster)/len(y_cluster))

        if (y_center not in self.y_range):
            on_target = 0
            if (y_center < self.y_range[0]):
                return 'up'
            else:
                return 'down'

        if (x_center not in self.x_range):
            on_target = 0
            if (x_center < self.x_range[0]):
                return 'left'
            else:
                return 'right'
        
        return 'center'
