import RPi.GPIO as gpio
import time
import os
from functools import reduce

targetPin = 14
pin2 = 23
pin3 = 24
pinIn = 4
pin4 = 16
pinInAlt = 26
pinInOut = 12

def setUp(pins=None, ins = None):
    gpio.setmode(gpio.BCM)
    if(pins is None):
        gpio.setup(targetPin, gpio.OUT)    
    else:
        for pin in pins:
            print(f'setting pin: {pin}')
            gpio.setup(pin, gpio.OUT)
    if(ins is not None):
        for p in ins:
            print(f'pin {p} is input')
            gpio.setup(p, gpio.IN, pull_up_down=gpio.PUD_UP)

def toggle(pin=targetPin ,stallTime = 1):
    gpio.output(pin, gpio.HIGH)
    time.sleep(stallTime)
    gpio.output(pin, gpio.LOW)
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
    setUp([targetPin])
    toggleTimes = intTryParse(input('how many toggle times: '))
    print(f"toggling {toggleTimes} times")
    for x in range(0, toggleTimes):
        toggle()
    cleanUp()

def lightPin(pin):
    gpio.output(pin, gpio.HIGH)
    time.sleep(1)
    gpio.output(pin, gpio.LOW)

def countDown():
    pins = [pin3, pin2, targetPin]
    setUp(pins)
    input('go?')
    for pin in pins:
        lightPin(pin)
    cleanUp()

def beep(pin, state):
    ##gpio.output(pin4, state)
    if(state is gpio.HIGH):
        print('BEEP')
    
def green(state):
    beep(pin4, state)
    gpio.output(targetPin, state)
    time.sleep(.2)
    gpio.output(pin2, state)
    time.sleep(.2)
    gpio.output(pin3, state)

def isPressed(state):
    return state is 0

def buttonReader():
    setUp(pins=[targetPin, pin2, pin3, pin4] ,ins=[pinIn])
    while True:
        input_state = gpio.input(pinIn)
        volt = gpio.HIGH if isPressed(input_state) else gpio.LOW
        green(volt)
            
def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    temp = (temp.replace("temp=", ""))
    temp = (temp.replace("'C", ""))
    return float(temp)

def switchAll(pins, state=gpio.LOW):
    for pin in pins:
        gpio.output(pin, state)

def onlyLightOne(on, offs, showLight):
    if showLight:
        switchAll(offs)
        gpio.output(on, gpio.HIGH)
    else:
        print(f'lighting: {on}')

def add(x,y): return x+y

def readHeat():
    setUp(pins=[targetPin, pin2, pin3] ,ins=[pinIn, pinInAlt, pinInOut])
    showLight = False
    temps = []
    currentTemp = measure_temp()
    temps.append(currentTemp)
    runLoop = True
    while runLoop:
        if isPressed(gpio.input(pinInOut)):
            runLoop = False
        else:
            if isPressed(gpio.input(pinIn)):
                showLight = True
            if isPressed(gpio.input(pinInAlt)):
                showLight = False
                switchAll([targetPin, pin2, pin3])
            currentTemp = measure_temp()
            if currentTemp > 46.2:
                onlyLightOne(pin3, [targetPin, pin2], showLight)
            elif currentTemp < 45.4:
                onlyLightOne(targetPin, [pin2, pin3], showLight)
            else:
                onlyLightOne(pin2, [targetPin, pin3], showLight)
            temps.append(currentTemp)
            if(len(temps) > 100):
                temps.pop(0)
            avg = (reduce(add, temps))/len(temps)
            ##print(f'Current temp is {currentTemp}, the average temp is {avg}')
            time.sleep(1)
    cleanUp()


readHeat()    






        
