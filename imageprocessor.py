import io
from PIL import Image
import threading
import picamera

class ImageStreamThread(threading.Thread):
    def __init__(self, shutdown_handlers):
        super(ImageStreamThread, self).__init__()

        shutdown_handlers.append(self.shutdown)

        self.terminated = False
        self.cam = picamera.PiCamera()
        self.cam.resolution = (50, 40)

        self.stream = io.BytesIO()

        self.start()

    def get_resolution(self):
        return self.cam.resolution

    def get_stream(self):
        return self.stream

    def shutdown(self):
        self.terminated = 1

    def run(self):
        while not self.terminated:
            self.stream.seek(0)
            self.cam.capture(self.stream, format='jpeg', use_video_port=True)


class ImageProcessor():
    def __init__(self, img_stream_thr):
        self.res_w, self.res_h = img_stream_thr.get_resolution()

        self.img_stream_thr = img_stream_thr

        self.x_range = range(round(self.res_w / 2 - 1), round(self.res_w / 2 + 1))
        self.y_range = range(round(self.res_h / 2 - 1), round(self.res_h / 2 + 1))

    def target_destroyed(self):
        #self.img_stream_thr.terminated = True

    def get_target_loc(self):
        pixels = Image.open(self.img_stream_thr.stream).load()
        return self.calc_target_loc(pixels)

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
