import time, logging
from gpiozero import LED, DistanceSensor
from enum import Enum # TODO

LOGGING_FILE_LOCATION = "coolRoom.log"


logging.basicConfig(filename=LOGGING_FILE_LOCATION,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    filemode='w',
                    level=logging.INFO)
safetyCarLogger = logging.getLogger()

DISTANCE_DETECTOR_LEDS = [LED(10), LED(11), LED(12), LED(13), LED(14), LED(15)] # green 1, green 2, orange 1, orange 2, red 1, red 2
DISTANCE_SENSORS = [DistanceSensor(21,22), DistanceSensor(23,24)]
ERROR_LED = LED(16)
COLLISSION_ALARM = LED(17)
DISTANCE_SENSORS_LEDS_THRESHOLD = [60, 50, 40, 30, 20, 10, 5]


previousTime = 0
waitTime = 1
if time.time() - previousTime >= waitTime:
    ...

# class ...(Enum):
#     ...
def blink(led: LED, blinkStatus: bool):
        if blinkStatus:
            led.on()
        else:
            led.off()

class DistanceDetector:
    def __init__(self, distanceSensors: list[DistanceSensor, DistanceSensor], distanceSensorLeds: list, distanceSensorsLedsThreshold: list, errorLed: LED, collissionAlarm) -> None:
        self.distanceSensors = distanceSensors
        self.distanceSensorsLeds = distanceSensorLeds
        self.errorLed = errorLed
        self.collissionAlarm = collissionAlarm
        self.previousBlinkTime = time.time()
        self.previousErrorLedBlinkTime = time.time()
        self.distanceSensorsReadings = [-1, -1]
        self.distanceSensorsLedsThreshold = distanceSensorsLedsThreshold
        self.distanceSensorsLedsBlinkStatus = False
        self.errorLedBlinkStatus = False
    
    def readSensors(self):
        for index, distanceSensor in enumerate(self.distanceSensors):
            self.distanceSensorsReadings[index] = distanceSensor.distance
        self.compareSensorResult()
    
    def compareSensorResult(self):
        if abs(self.distanceSensorsReadings[0] - self.distanceSensorsReadings[1]) >= 5:
            self.blinkErrorLed()
        self.averageSensorReading = self.calculateAverageSensorValue()
        self.updateDistanceLedStatus()
          
    def calculateAverageSensorValue(self):
        return sum(self.distanceSensorsReadings) / len(self.distanceSensorsReadings)
        
    def blinkErrorLed(self):
        if time.time() - self.previousErrorLedBlinkTime > 0.1:
            blink(self.errorLed, self.errorLedBlinkStatus)
            self.errorLedBlinkStatus = not self.errorLedBlinkStatus   
            
    def updateDistanceLedStatus(self):
        if not self.isCloserThan5cm():
            for index, threshold in enumerate(self.distanceSensorsLedsThreshold):
                if threshold < self.averageSensorReading:
                    blink(self.distanceSensorsLeds[index], self.distanceSensorsLedsBlinkStatus)
            self.distanceSensorsLedsBlinkStatus = not self.distanceSensorsLedsBlinkStatus
        else:
            self.ledsShowCloseReading()
            
    def isCloserThan5cm(self):
        if self.averageSensorReading < 5:
            return True
        return False
            
    def ledsShowCloseReading(self): # TODO change name
        for led in self.distanceSensorsLeds:
            led.on()

    
SAFE_CAR = DistanceDetector(DISTANCE_SENSORS, DISTANCE_DETECTOR_LEDS, ERROR_LED, COLLISSION_ALARM)  
    
    
while True:
    SAFE_CAR.readSensors()
    
    
    

