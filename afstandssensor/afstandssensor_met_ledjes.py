from gpiozero import DistanceSensor, LED
from time import time

ledPins = [2,3,4,5,6]
ledArray = []
for nummer in range(5):
    ledArray.append(LED(ledPins[nummer]))

sensor = DistanceSensor(23,24)

activatieOp = [0.2, 0.4, 0.6, 0.8, 0.99]

while True:
    currentTime = time()
    sensorReading = sensor.distance
    
    for index, afstand in enumerate(activatieOp):
        if sensorReading > afstand:
            ledArray[index].off()
        else:
            ledArray[index].on()
    print(f"afstand tot object is {sensor.distance}m")


