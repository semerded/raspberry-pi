"""
Deel 1 
Op een RPi zitten twee DHT11 temperatuursensoren aangesloten die de temperatuur van een koelinstallatie meten. Van beide sensoren wordt het gemiddelde genomen. Met 6 led creëer je een thermometer.

Deel 2 
Een drukknop kijkt of de deur van de koeling open staat. De drukknop is aangesloten met een interne pull-up weerstand van de RPi. Als de deur van de koeling open staat gaat er een rode led knipperen 1 s aan, 1 s uit. Gebruik geen sleep.

Deel 3 
Volgende data wordt geprint met een tijdstempel in een file: 

Gemiddelde temperatuur elke keer als deze verandert.  
Als de deur open gaat wordt dit gemeld. 
Als de deur sluit wordt dit ook gemeld. 
"""

import time, logging, Adafruit_DHT, threading, enum
from gpiozero import LED, Button

LOGGING_FILE_LOCATION = "DHT11log.txt"


logging.basicConfig(filename=LOGGING_FILE_LOCATION,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    filemode='w',
                    level=logging.INFO)
coolRoomLogger = logging.getLogger()

COOL_ROOM_DOOR_SENSOR = Button(11)

THERMOMETER_LEDS = [LED(10),LED(11),LED(12),LED(13),LED(14),LED(15),]
THERMOMETER_LEDS_THRESHOLD = [-6,-3,0,3,6,9]
COOL_ROOM_DOOR_OPEN_INDICATOR_LED = LED(16)

def valuesNotNone(valueSensor1, ValueSensor2):
    isValueNotNone = True
    if valueSensor1 == None:
        coolRoomLogger.error("sensor 1 reads 'None'")
        isValueNotNone = False
    if ValueSensor2 == None:
        coolRoomLogger.error("sensor 2 reads 'None'")
        isValueNotNone = False
    return isValueNotNone

class doorPosition(enum):
    IsOpen = True
    IsClosed = False


class ColdRoom:
    def __init__(self) -> None:
        self.averageTemperature = None
        self.doorPosition = doorPosition.IsClosed
        self.loggedAtstatus = None   

    def measureTemperatureInColdRoom(self): # running in different thread
        while True:
            unused_humidity, DHTtemperature_sensor1 = Adafruit_DHT.read(Adafruit_DHT.DHT11, 4)
            unused_humidity, DHTtemperature_sensor2 = Adafruit_DHT.read(Adafruit_DHT.DHT11, 5)
            if valuesNotNone(DHTtemperature_sensor1, DHTtemperature_sensor2):
                self.averageTemperature = (DHTtemperature_sensor1 + DHTtemperature_sensor2) / 2
                coolRoomLogger.info("average temperature is %s" %self.averageTemperature)
            else:
                coolRoomLogger.warning("unable to update thermometer because a sensor reads None")
            time.sleep(2)
    
    def updateThermometer(self): 
        if self.averageTemperature is not None: # none when sensors are not initiated
            for ledNumber, thresholdValue in enumerate(THERMOMETER_LEDS_THRESHOLD): 
                if self.averageTemperature > thresholdValue:
                    THERMOMETER_LEDS[ledNumber].on()
                else:
                    THERMOMETER_LEDS[ledNumber].off()
                    
    def logDoorStatus(self, doorPosition: doorPosition):
        doorPosition = doorPosition.value
        if doorPosition != self.loggedAtstatus:
            logDoorValue = "opened" if doorPosition else "closed"
            coolRoomLogger.info("door is %s" %logDoorValue)
            self.loggedAtstatus = doorPosition
                    
    def checkDoor(self):
       if COOL_ROOM_DOOR_SENSOR.is_active:
            self.doorPosition = doorPosition.IsClosed
            self.logDoorStatus(doorPosition.IsClosed)
       else:
            self.doorPosition = doorPosition.IsOpen
            self.logDoorStatus(doorPosition.IsOpen)

        
    def doorWaringLight(self): 
        # if currentTime - self.previousBlinkTime > self.blinkTimeInSec:
            COOL_ROOM_DOOR_OPEN_INDICATOR_LED.blink(1)
                      
COLDROOM = ColdRoom()
                
def main():
    while True:
        # currentTime = time.time()
        COLDROOM.updateThermometer()
        COLDROOM.checkDoor()
        if COLDROOM.doorOpen:
            COLDROOM.doorWaringLight()

temperatureMeasurementThread = threading.Thread(target=COLDROOM.measureTemperatureInColdRoom, args=())
mainThread = threading.Thread(target=main, args=())

temperatureMeasurementThread.start()
mainThread.start()
