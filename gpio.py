import RPi.GPIO as gpio
import time

targetPin = 14

def setUp():
    gpio.setmode(gpio.BCM)
    gpio.setup(targetPin, gpio.OUT)

def toggle(stallTime = 1):
    gpio.output(targetPin, gpio.HIGH)
    time.sleep(stallTime)
    gpio.output(targetPin, gpio.LOW)
    time.sleep(stallTime)

def cleanUp():
    gpio.cleanup()

def intTryParse(value):
    try:
        return int(value)
    except ValueError:
        print('error in parseing the value')
        return 0

##def setUp():
##    print('set up')
##
##def toggle(stallTime = 1):
##    print(f"stall time is :{stallTime}")
##
##def cleanUp():
##    print('cleaning up')

def run():
    setUp()
    toggleTimes = intTryParse(input('how many toggle times: '))
    print(f"toggling {toggleTimes} times")
    for x in range(0, toggleTimes):
        toggle()
    cleanUp()

run()
