from gpiozero import InputDevice
from time import time, ctime
from os.path import isfile
import Adafruit_DHT

BUTTON = InputDevice(11)

FILELOCATION = "savefile.txt"

writeData = False
previousTime = 0
timeBetweenLog = 5

if isfile(FILELOCATION) is False:
    file = open(FILELOCATION, "w")
    file.close()
    del file

while True:
    currentTime = time()
    
    if BUTTON.is_active:
        writeData = not writeData
        if writeData:
            print("data loging started")
        else:
            print("data loging stopped")
    if writeData:
        if currentTime - previousTime > timeBetweenLog:
            vochtigheid, temperatuur = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
            print("data loged")
            
            
            with open(FILELOCATION, "a") as saveFile:
                saveFile.writelines(f"{ctime} | temperature: {temperatuur}°C | humidity: {vochtigheid}%")