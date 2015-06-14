import io
import RPi.GPIO as GPIO
from PIL import Image
import threading


class Camera(threading.Thread):
    def __init__(self, picam):
        super(Camera, self).__init__()
        self.picam = picam
        self.terminated = False
        self.stream = io.BytesIO()
        self.start()

    def get_stream(self):
        return self.stream

    def shutdown_procedure(self):
        print("shutdown camera")
        self.terminated = 1

    def run(self):
        while not self.terminated:
            self.stream.seek(0)
            self.picam.capture(self.stream, format='jpeg', use_video_port=True)


class TargetLocator():
    def __init__(self, resolution):
        self.res_w, self.res_h = resolution

        self.x_range = range(round(self.res_w / 2 - 1), round(self.res_w / 2 + 1))
        self.y_range = range(round(self.res_h / 2 - 1), round(self.res_h / 2 + 1))

    def get_target_loc(self, stream):
        pixels = Image.open(stream).load()
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

        
class Pin:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def shutdown_procedure(self):
        self.off()
        GPIO.cleanup(self.pin)
        print("Shutdown complete: Pin # %s" % self.pin)
