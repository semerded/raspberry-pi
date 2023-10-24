import gpiozero as io
from time import time, ctime
from os.path import isfile
import Adafruit_DHT

BUTTON = io.Button(11)

FILELOCATION = "DHT11log.txt"

writeData = False
previousTime = 0
timeBetweenLog = 5

if isfile(FILELOCATION) is False:
    file = open(FILELOCATION, "w")
    file.close()
    del file
    
def stateChangeDetection():
    global writeData, previousTime, currentTime
    writeData = not writeData
    previousTime = currentTime
    if writeData:
        print("data logging started")
    else:
        print("data logging stopped")

print("Sensor reader started (logging turned off)")
while True:
    currentTime = time()
    
    BUTTON.when_activated = stateChangeDetection
    if writeData:
        vochtigheid, temperatuur = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4, 2)
        if currentTime - previousTime > timeBetweenLog:
            if vochtigheid != None and temperatuur != None:
                with open(FILELOCATION, "a") as saveFile:
                    logTime = ctime()
                    print("data loged at %s" % logTime)
                    saveFile.write(f"{logTime} | temperature: {temperatuur}°C | humidity: {vochtigheid}%\n")
                previousTime = currentTime
            else:
                print("failed to read sensor")