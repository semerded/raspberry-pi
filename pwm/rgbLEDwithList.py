import RPi.GPIO as IO, time
    
IO.setmode(IO.BCM)
IO.setwarnings(False)

RGB_LIST = [(255,0,0),
            (255,140,0),
            (255,215,0),
            (255,255,0),
            (173,255,47),
            (124,252,0	),
            (0,255,0	),
            (0,250,154	),
            (127,255,212	),
            (0,245,255	),
            (187,255,255	),
            (0,255,255	),
            (0,191,255	),
            (0,0,255),
            (0,0,205),
            (25,25,112	),
            (138,43,226),
            (186,85,211	),
            (255,131,250	),
            (255,62,150	),
            (255,182,193),
            (245,222,179	),
            (255,255,255),
            ]

class RGB_LED:
    def __init__(self, pinRed: int, pinGreen: int, pinBlue: int) -> None:
        self.pinRed = pinRed
        self.pinGreen = pinGreen
        self.pinBlue = pinBlue
        self.pinListing = {self.pinRed: None, self.pinGreen: None, self.pinBlue: None}
        self.listIndex = 0
        self.RGBlist = []
        self._IOsetup()        
        
    def _IOsetup(self):
        for pin in self.pinListing:
            IO.setup(pin, IO.OUT)
            self.pinListing[pin] = IO.PWM(pin, 100)
            self.pinListing[pin].start(0)
            
    def setList(self, RGBlist: list[tuple]):
        self.RGBlist = RGBlist
            
    def colorListCycle(self):
        self._checkListIndexOverflow()
        self.updateLEDs()
        self.listIndex += 1
            
    def _checkListIndexOverflow(self):
        if (listLenght := len(self.RGBlist)) != 0 and self.listIndex == listLenght -1:
            self.listIndex = 0 
                
    def updateLEDs(self):
        currentColor = self.RGBlist[self.listIndex]
        for index, pwm in enumerate(self.pinListing.values()):
            pwm.ChangeDutyCycle(currentColor[index] / 2.55)

rgb_LED = RGB_LED(12, 13, 18)
rgb_LED.setList(RGB_LIST)

while True:
    rgb_LED.colorListCycle()
    time.sleep(0.2)