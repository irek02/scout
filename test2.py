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


'''
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