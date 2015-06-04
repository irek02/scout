class Vehicle:
	def __init__(self, img_processor):
    	self.img_processor = img_processor
    	self.on_target = 0
    	self.target_engaged = False

    def seek_and_destroy(self):
    	while not target_engaged:
	    	target_loc = img_processor.get_target_loc()

	    	if not target_loc:
	    		print("Target not found")
	    		continue

	    	if target_loc == 'center':
	    		if (on_target == 0):
			        on_target = time.time()
			        GPIO.output(pin_led, GPIO.HIGH)
			        continue
			    elif (time.time() - on_target > target_lock_time):
			        engage_target()
			        on_target = 0
			        print('Target engaged.')
			        return

	    	if target_loc in ['up', 'down', 'left', 'right']:
	    		move(target_loc)
	    		continue

	def engage_target(self):
		GPIO.output(pin,GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(pin,GPIO.LOW)
		GPIO.output(pin_led, GPIO.LOW)
		target_engaged = True


	

	def move(self, direction):
		# Implement flight control here
		direction
