import os
import time
from functools import reduce

#

def measure_temp():
	temp = os.popen("vcgencmd measure_temp").readline()
        temp = (temp.replace("temp=", ""))
        temp = (temp.replace("'C", ""))
        return float(temp)

def add(x,y): return x+y

temps = []
while True:
        currentTemp = measure_temp()
        temps.append(currentTemp)
        if(len(temps) > 100):
                temps.pop(0)
        avg = (reduce(add, temps))/len(temps)
        print("Current temp is {}, the average temp is {}".format(currentTemp, avg))
        time.sleep(30)
