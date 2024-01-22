import RPi.GPIO as IO, time
from enum import Enum

class colorStatus(Enum):
    static = 0
    ascend = 1
    descend = 1
    
class outOf8bitRange(Exception): ...

IO.setmode(IO.BCM)
IO.setwarnings(False)

class RGB_LED:
    def __init__(self, pinRed: int, pinGreen: int, pinBlue: int) -> None:
        self.pinRed = pinRed
        self.pinGreen = pinGreen
        self.pinBlue = pinBlue
        self.pinListing = {self.pinRed: None, self.pinGreen: None, self.pinBlue: None}
        self.colorValue = [0, 0, 0]
        self.colorValueStatus = [colorStatus.ascend, colorStatus.static, colorStatus.static]
        self._IOsetup()        
        
    def _IOsetup(self):
        for pin in self.pinListing:
            IO.setup(pin, IO.OUT)
            self.pinListing[pin] = IO.PWM(pin, 100)
            self.pinListing[pin].start(0)
            
    def colorCycle(self):
        self.checkValues()
        self._updateColorCycleValues()
        self.updateLEDs()
       
                
    def checkValues(self):
        for index, colorValue in enumerate(self.colorValue):
            if colorValue >= 255:
                self.colorValueStatus[index] = colorStatus.descend
                self._updateNextIndex(index, colorStatus.ascend)
            
            if colorValue == 0 and self.colorValueStatus[index] == colorStatus.descend:
                self.colorValueStatus[index] = colorStatus.static

    def _updateNextIndex(self, index, value):
        try:
            self.colorValueStatus[index + 1] = value
        except IndexError:
            self.colorValueStatus[0] = value
            
            
        
    def _updateColorCycleValues(self):
        for index, status in enumerate(self.colorValueStatus):
            if status == colorStatus.ascend:
                self.colorValue[index] += 1
                
            if status == colorStatus.descend:
                self.colorValue[index] -= 1
                
    def updateLEDs(self):
        for index, pwm in enumerate(self.pinListing.values()):
            pwm.ChangeDutyCycle(self.colorValue[index])

        
    def setValue(self, colorRed, colorGreen, colorBlue):
        if self.checkForOutOfRangeError(colorRed) or self.checkForOutOfRangeError(colorGreen) or self.checkForOutOfRangeError(colorBlue):
            raise outOf8bitRange("set value is out of the 0-255 rgb value range")
        self.colorValue = [colorRed, colorGreen, colorBlue]
        
    def checkForOutOfRangeError(input):
        if input not in range(0, 256):
            return True
        return False
        
        
            
        
        


rgb_LED = RGB_LED(12, 13, 14)

while True:
    rgb_LED.colorCycle()
    time.sleep(0.1)