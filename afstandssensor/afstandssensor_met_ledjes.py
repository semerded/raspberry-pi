from gpiozero import DistanceSensor, LED
from time import time

ledPins = [2,3,4,5,6]
ledArray = []
for nummer in range(5):
    ledArray.append(LED(ledPins[nummer]))
    

sensor = DistanceSensor(23,24)

previousTime = time()
activatieOp = [0.2, 0.4, 0.6, 0.8, 1]
delay = 0.5

while True:
    currentTime = time()
    
    if currentTime - previousTime > delay:
        for index, afstand in enumerate(activatieOp):
            if sensor.distance > afstand:
                ledArray[index].on()
            else:
                ledArray[index].off()
        print(f"afstand tot object is {sensor.distance}m")
        

