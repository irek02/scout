import time
import RPi.GPIO as GPIO

class Vehicle:
    def __init__(self, img_processor):
        self.img_processor = img_processor
        self.on_target = 0
        self.target_engaged = False
        self.target_lock_time = 2
        self.led = Pin(15)
        self.laser = Pin(18)
        
    def seek_and_destroy(self):
        print("seek")
        while not self.target_engaged:

            time.sleep(0.5)
            target_loc = self.img_processor.get_target_loc()

            if not target_loc:
                #print("Target not found")
                continue

            if target_loc == 'center':
                self.led.on()
                if (self.on_target == 0):
                    self.on_target = time.time()
                elif (time.time() - self.on_target > self.target_lock_time):
                    self.engage_target()
                    on_target = 0
                    print('Target engaged.')
                    break
                continue

            self.led.off()

            if target_loc in ['up', 'down', 'left', 'right']:
                self.move(target_loc)
                continue

    def engage_target(self):
        self.laser.on()
        time.sleep(0.5)
        self.laser.off()
        self.led.off()
        self.target_engaged = True

        self.img_processor.terminated = True

    def move(self, direction):
        # Implement flight control here
        direction

class Pin:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
