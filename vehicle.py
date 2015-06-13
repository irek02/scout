import time

class Vehicle:
    def __init__(self, camera, target_loc, led, laser):
        self.camera = camera
        self.target_loc = target_loc
        self.led = led
        self.laser = laser

        self.on_target = 0
        self.target_engaged = False
        self.target_lock_time = 2
        
    def seek_and_destroy(self):
        print("seek")
        while not self.target_engaged:

            time.sleep(0.5)
            stream = self.camera.get_stream()
            target_loc = self.target_loc.get_target_loc(stream)

            print(target_loc)

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
            
            self.on_target = 0
            self.led.off()

            if target_loc in ['up', 'down', 'left', 'right']:
                self.move(target_loc)
                continue

        self.shutdown_procedure()

    def engage_target(self):
        self.laser.on()
        time.sleep(0.5)
        self.laser.off()
        self.led.off()
        self.target_engaged = True

    def move(self, direction):
        # Implement flight control here
        direction

    def shutdown_procedure(self):
        self.camera.shutdown_procedure()
        self.led.shutdown_procedure()
        self.laser.shutdown_procedure()
