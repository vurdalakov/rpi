import RPi.GPIO as gpio
import time
import threading

LED_PIN = 12 # led connected to GPIO18
BUTTON_PIN = 13 # button connected to GPIO27

exitFlag = 1
thread = None

# blinking function
def blink(pin):
    gpio.output(pin, gpio.HIGH)
    time.sleep(2)
    gpio.output(pin, gpio.LOW)
    time.sleep(1)
    return

# thread class
class blink_thread(threading.Thread):
    def __init__(self, pin):
        threading.Thread.__init__(self)
        self.pin = pin
    def run(self):
        while not exitFlag:
            blink(self.pin)

def main():
    # use board pin numbers
    gpio.setmode(gpio.BOARD)

    # set up gpio.pins
    gpio.setup(LED_PIN, gpio.OUT)
    gpio.setup(BUTTON_PIN, gpio.IN)

    global exitFlag
    global thread
    while True:
        if not gpio.input(BUTTON_PIN):
            if exitFlag:
                exitFlag = 0
                thread = blink_thread(LED_PIN)
                thread.start()
            else:
                exitFlag = 1
            time.sleep(1)
        time.sleep(0.1)

try:
    main()
except KeyboardInterrupt:
    print
    exitFlag = 1
    if not thread is None:
        thread.join()
        print "Waiting for blink thread"
    gpio.cleanup()
    print "Done"
