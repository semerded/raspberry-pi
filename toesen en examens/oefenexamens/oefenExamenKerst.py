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

import time, logging, Adafruit_DHT, threading
from gpiozero import LED, Button
from enum import Enum

LOGGING_FILE_LOCATION = "coolRoom.log"


logging.basicConfig(filename=LOGGING_FILE_LOCATION,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    filemode='w',
                    level=logging.INFO)
coolRoomLogger = logging.getLogger()

# start logger
coolRoomLogger.info("cool room started at %s" %time.ctime())
coolRoomLogger.info("-"*50)

COOL_ROOM_DOOR_SENSOR = Button(9)

THERMOMETER_LEDS = [LED(10),LED(11),LED(12),LED(13),LED(14),LED(15),]
THERMOMETER_LEDS_THRESHOLD = [-6,-3,0,3,6,9]
# THERMOMETER_LEDS_THRESHOLD = [18,20,22,24,26,28] # uncomment this for test vars
COOL_ROOM_DOOR_OPEN_INDICATOR_LED = LED(16)

class doorPosition(Enum):
    IsOpen = True
    IsClosed = False


class ColdRoom:
    def __init__(self) -> None:
        self.averageTemperature = None
        self.doorPosition = doorPosition.IsClosed
        self.loggedAtstatus = None  
        self.previouseAverageTemperature = None 
        self.invalidReadingInArow = 0
        self.blinkTimeInSec = 1
        self.previousBlinkTime = 0
        self.coolRoomDoorIndicatorLed = False
        
    def checkIfDHTsensorsReadTemp(valueSensor1, ValueSensor2):
        if valueSensor1 == None:
            isValueSensor1NotNone = False
        else:
            isValueSensor1NotNone = True
        if ValueSensor2 == None:
            isValueSensor2NotNone = False
        else:
            isValueSensor2NotNone = True
        return (isValueSensor1NotNone, isValueSensor2NotNone)



    def measureTemperatureInColdRoom(self): # running in different thread
        while True:
            # read DHT11 sensors
            unused_humidity, DHTtemperature_sensor1 = Adafruit_DHT.read(Adafruit_DHT.DHT11, 4)
            unused_humidity, DHTtemperature_sensor2 = Adafruit_DHT.read(Adafruit_DHT.DHT11, 5)
            
            # check if both sensors read a temperature and not none
            resultOfValidationCheck = self.checkIfDHTsensorsReadTemp(DHTtemperature_sensor1, DHTtemperature_sensor2)
            
            if resultOfValidationCheck[0] and resultOfValidationCheck[1]:
                self.invalidReadingInArow = 0
                self.averageTemperature = (DHTtemperature_sensor1 + DHTtemperature_sensor2) / 2
                if self.averageTemperature != self.previouseAverageTemperature:
                    coolRoomLogger.info("average temperature changed to %s°C" %self.averageTemperature)
                    self.previouseAverageTemperature = self.averageTemperature
                time.sleep(2)
                
            else: # if a sensor reads 0: retry until it reads a temp
                self.invalidReadingInArow += 1
                if self.invalidReadingInArow >= 5: # if the sensor fails to read 5 or more times: give an error log message
                    coolRoomLogger.warning(f"unable to update thermometer because a sensor reads None (valid Temp: sensor 1: {resultOfValidationCheck[0]} | sensor 2: {resultOfValidationCheck[1]})")
    
    def updateThermometer(self): 
        if self.averageTemperature is not None: # none when sensors are not initiated
            for ledNumber, thresholdValue in enumerate(THERMOMETER_LEDS_THRESHOLD): 
                if self.averageTemperature >= thresholdValue:
                    THERMOMETER_LEDS[ledNumber].on()
                else:
                    THERMOMETER_LEDS[ledNumber].off()
                    
    def logDoorStatus(self, doorPosition: doorPosition):
        # only log when door positon is changed
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

        
    def blinkDoorWaringLight(self): 
        # an implementation of the blink function
        currentTime = time.time()
        if currentTime - self.previousBlinkTime > self.blinkTimeInSec:
            self.coolRoomDoorIndicatorLed = not self.coolRoomDoorIndicatorLed
            if self.coolRoomDoorIndicatorLed:
                COOL_ROOM_DOOR_OPEN_INDICATOR_LED.on()
            else:
                COOL_ROOM_DOOR_OPEN_INDICATOR_LED.off()
            self.previousBlinkTime = currentTime
    
    @property
    def getDoorPosition(self):
        return self.doorPosition.value
                      
COLDROOM = ColdRoom() # TODO add parameters to class init to make it reusable for multiple coldrooms
                
def main(): # function for main thread
    while True:
        COLDROOM.updateThermometer()
        
        COLDROOM.checkDoor()
        if COLDROOM.getDoorPosition:
            COLDROOM.blinkDoorWaringLight()
        else: 
            COOL_ROOM_DOOR_OPEN_INDICATOR_LED.off()

temperatureMeasurementThread = threading.Thread(target=COLDROOM.measureTemperatureInColdRoom, args=()) # temperature reading thread
mainThread = threading.Thread(target=main, args=()) # main thread

# start the threads
temperatureMeasurementThread.start()
mainThread.start()
