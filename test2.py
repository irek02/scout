res_w = 100
res_h = 90
x_range = range(round(res_w / 2 - 10), round(res_w / 2 + 10))
y_range = range(round(res_h / 2 - 10), round(res_h / 2 + 10))
grid = []
i = 0

f = open('/home/pi/scripts/tmp.txt', "w+")


for y in range(1, res_h):
	f.write("\n")
	for x in range(1, res_w):
		f.write('(' + str(i) + ') ')
		grid.insert(i, (x, y))
		i = i + 1

print(len(grid))
print(grid[2183])
f.close()

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