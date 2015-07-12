import RPi.GPIO as GPIO

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
