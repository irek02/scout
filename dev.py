import os.path
import picamera
import io
from PIL import Image
import components
import time




resolution = (50, 40)
locator = components.TargetLocator(resolution)
img = Image.open('left.jpg')
pixels = img.load()
print(locator.calc_target_loc(pixels))

'''
try:
    with picamera.PiCamera() as camera:
        camera.resolution = resolution
        stream = io.BytesIO()

        parser = components.StreamParser()

        #camera.capture(stream, use_video_port=True)
        for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            time.sleep(0.8)
            img = Image.open(stream)
            

            loc = locator.get_target_loc(stream)
            if (loc == 'right'):
                img.save('right.jpg')
                break
            
            print(loc)
            # Truncate the stream to the current position (in case
            # prior iterations output a longer image)
            stream.truncate()
            stream.seek(0)
            if False:
                break

except:
    f.close()

'''
'''


f = open('/home/pi/scripts/tmp.txt', "rb")
bytes = f.read()
# stream = io.BytesIO(bytes)
loc = locator.get_target_loc(bytes)
f.close()



class ImageProcessor:
    def get_loc(self):
    	return 'up'
    	


class Vehicle:
	def __init__(self, img_processor):
		self.img_processor = img_processor

	def seek_and_destroy(self):
		return img_processor.get_loc()


img_processor = ImageProcessor()
veh = Vehicle(img_processor)

print veh.seek_and_destroy()



from PIL import Image
w = 640
h = 480

w_center = w / 2
h_center = h / 2

tolerance_factor = 0.1

w_tolerance = round(w * tolerance_factor)
h_tolerance = round(h * tolerance_factor)

center = list()
f = open('/home/pi/scripts/tmp.txt', "w+")

for x in range(round(w_center - w_tolerance), round(w_center + w_tolerance)):
	for y in range(round(h_center - h_tolerance), round(h_center + h_tolerance)):
		center.append(x * y)
		


img = Image.open('../img1.jpg')

left = int(w_center - w_tolerance)
upper = int(h_center - h_tolerance)
right = int(w_center + w_tolerance)
lower = int(h_center + h_tolerance)

box = (left, upper, right, lower)

region = img.crop(box)
region.save('../img2.jpg')

f.close()
'''

'''
h_pxl = 0
while h_pxl <= h:
	f.write("\n")
	h_pxl = h_pxl + 1
	w_pxl = 0
	while w_pxl <= w:
		w_pxl = w_pxl + 1
		f.write(str(i) + ', ')
		i = i + 1

f.close()
'''