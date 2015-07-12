import io
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
