import io
from PIL import Image
import threading

class ImageProcessor:
    
    def __init__(self, camera):
        self.stream = io.BytesIO()
        self.target_loc = None
        self.res_w, self.res_h = camera.resolution
        self.x_range = range(round(self.res_w / 2 - 1), round(self.res_w / 2 + 1))
        self.y_range = range(round(self.res_h / 2 - 1), round(self.res_h / 2 + 1))
        camera.capture_sequence(self.stream_generator(), use_video_port=True)

    def stream_generator(self):


        t = threading.Thread(target=self.foo)
        t.start()

        '''
        while True:
            print("Loop")
            self.stream.truncate()
            self.stream.seek(0)
            yield self.stream
            self.target_loc = self.calc_target_loc()
            '''

    def foo(self):
        while True:
            print("Loop")
            self.stream.truncate()
            self.stream.seek(0)
            yield self.stream
            self.target_loc = self.calc_target_loc()

    def get_target_loc(self):
        return self.target_loc

    def getPixels(self):
        return Image.open(self.stream).load()

    def calc_target_loc(self):
     
        pixels = self.getPixels()
        
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