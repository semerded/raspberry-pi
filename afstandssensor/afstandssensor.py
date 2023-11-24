from gpiozero import DistanceSensor
from time import time


sensor = DistanceSensor(23,24)

previousTime = time()
delay = 1

while True:
    currentTime = time()
    
    if currentTime - previousTime > delay:
        print(f"afstand tot object is {round(sensor.distance * 100, 2)}cm")

