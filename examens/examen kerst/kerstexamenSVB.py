import time, logging, threading
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
DISTANCE_SENSORS_LEDS_THRESHOLD = [0.60, 0.50, 0.40, 0.30, 0.20, 0.10]


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
        self.currentTime = time.time()
        self.previousBlinkTime = self.currentTime
        self.previousErrorLedBlinkTime = self.currentTime
        self.distanceSensorsReadings = [-1, -1]
        self.distanceSensorsLedsThreshold = distanceSensorsLedsThreshold
        self.distanceSensorsLedsBlinkStatus = False
        self.errorLedBlinkStatus = False
        self.averageSensorReading = -1
        
    def main(self):
        while True:
            self.currentTime = time.time()
            self.compareSensorResult()
        
  
    
    def readSensors(self):
        while True:
            for index, distanceSensor in enumerate(self.distanceSensors):
                self.distanceSensorsReadings[index] = distanceSensor.distance
            self.averageSensorReading = self.calculateAverageSensorValue()
    
    def compareSensorResult(self):
        if abs(self.distanceSensorsReadings[0] - self.distanceSensorsReadings[1]) >= 0.05:
            self.blinkErrorLed()
        else:
            self.updateDistanceLedStatus()
          
    def calculateAverageSensorValue(self):
        return sum(self.distanceSensorsReadings) / len(self.distanceSensorsReadings)
        
    def blinkErrorLed(self):
        self.ledsShowCloseReading()
        if self.currentTime - self.previousErrorLedBlinkTime > 0.1:
            blink(self.errorLed, self.errorLedBlinkStatus)
            self.errorLedBlinkStatus = not self.errorLedBlinkStatus
            self.previousErrorLedBlinkTime = self.currentTime
            
    def updateDistanceLedStatus(self):
        if not self.isCloserThan5cm():
            for index, threshold in enumerate(self.distanceSensorsLedsThreshold):
                if threshold < self.averageSensorReading:
                    blink(self.distanceSensorsLeds[index], self.distanceSensorsLedsBlinkStatus)
                else:
                    self.distanceSensorsLeds[index].off()
            if self.currentTime - self.previousBlinkTime > 0.5:
                self.distanceSensorsLedsBlinkStatus = not self.distanceSensorsLedsBlinkStatus
                self.previousBlinkTime = self.currentTime
        else:
            self.ledsShowCloseReading()
            
    def isCloserThan5cm(self):
        if self.averageSensorReading < 0.05:
            return True
        return False
            
    def ledsShowCloseReading(self): # TODO change name
        for led in self.distanceSensorsLeds:
            led.on()

    
SAFE_CAR = DistanceDetector(DISTANCE_SENSORS, DISTANCE_DETECTOR_LEDS, DISTANCE_SENSORS_LEDS_THRESHOLD, ERROR_LED, COLLISSION_ALARM)  
    
    
mainThread = threading.Thread(target=SAFE_CAR.main,args=())
distanceSensorThread = threading.Thread(target=SAFE_CAR.readSensors,args=())

mainThread.start()
distanceSensorThread.start()
    
    
    

