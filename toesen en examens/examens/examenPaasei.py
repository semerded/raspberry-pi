from gpiozero import Button, AngularServo, PWMOutputDevice
from threading import Thread
import Adafruit_DHT

running = True

# button
class RpiButton(Button):
    """
    remake om de `isClicked` functie toe te voegen
    """
    def __init__(self, pin=None, pull_up=True, active_state=None, bounce_time=None, hold_time=1, hold_repeat=False, pin_factory=None):
        super().__init__(pin, pull_up, active_state, bounce_time, hold_time, hold_repeat, pin_factory)
        self.alreadyClicked = False
        
    def isClicked(self):
        if self.is_active:
            if not self.alreadyClicked:
                self.alreadyClicked = True
                return True
        else:
            self.alreadyClicked = False
        return False

# mixer
class MixerController():
    mixerSpeedMapping: dict[int, int] = {1: 0, 2: 25, 3: 50, 4: 75, 5: 100}
    def __init__(self, motorPin: int, increaseSpeed: RpiButton, decreaseSpeed: RpiButton, confirm: RpiButton):
        self.mixMotor = PWMOutputDevice(motorPin)
        self.increaseSpeedButton: RpiButton = increaseSpeed
        self.decreaseSpeedButton: RpiButton = decreaseSpeed
        self.confirmSpeedButton: RpiButton = confirm
        self.currentSpeedStep: int = 1
        
    def mainLoop(self):
        self._readIncreaseButton()
        self._readDecreaseButton()
        self._readConfirmButton()
        
    def _readIncreaseButton(self):
        if self.increaseSpeedButton.isClicked() and self.currentSpeedStep < 5:
            self.currentSpeedStep += 1
            print("de snelheid is nu %s" %self.currentSpeedStep)
        
    def _readDecreaseButton(self):
        if self.decreaseSpeedButton.isClicked() and self.currentSpeedStep > 1:
            self.currentSpeedStep -= 1
            print("de snelheid is nu %s" %self.currentSpeedStep)
        
    def _readConfirmButton(self):
        if self.confirmSpeedButton.isClicked():
            self.mixMotor.value = self.mixerSpeedMapping[self.currentSpeedStep] / 100
            print("motorsnelheid is succesvol geupdate")
            
# humidity sensor
class DHT11:
    def __init__(self) -> None:
        self.humidity: float = 0
        self.temperature: float = 0

    def getHumidityAndTemperature(self):
        return self._readDataFromDHT()
    
    def getTemperature(self):
        return self._readDataFromDHT()[1]
    
    def getHumidity(self):
        return self._readDataFromDHT()[0]
    
    def _readDataFromDHT(self):
        _humidity, _temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4, 3) # lees de data van de DHT11 uit (2 staat voor hoevaak hij de data opnieuw zal proberen uit te lezen als er iets fout mocht gaan)
        if _humidity != None:
            self.humidity = _humidity
        if _temperature != None:
            self.temperature = _temperature
        return self.humidity, self.temperature

            
class HumidityController(DHT11):
    airChannelAngleMapping = {100: 170, 90: 135, 75: 90,  60: 45, 40: 10} # humidity level: angle of airchannel
    def __init__(self, servo: AngularServo) -> None:
        super().__init__()
        self.servo: AngularServo = servo

    def startThread(self): # threaded
        Thread(target=self._threadedMainLoop).start()
        
    def _threadedMainLoop(self):
        while running:
            self.mainLoop()
            
    def mainLoop(self):
        humidity = super().getHumidity()
        self.controlAirChannelWithHumidity(humidity)
        
    def controlAirChannelWithHumidity(self, humidity: float):
        for requiredHumidity, servoAngle in self.airChannelAngleMapping.items():
            if humidity >= requiredHumidity:
                self.servo.angle = servoAngle - 90
                break
                
# init classes
decreaseSpeedButton = RpiButton(5)
increaseSpeedButton = RpiButton(6)
confirmSpeedButton = RpiButton(21)

mixerController = MixerController(motorPin=12, increaseSpeed=increaseSpeedButton, decreaseSpeed=decreaseSpeedButton, confirm=confirmSpeedButton)

airChannelServo = AngularServo(17)

humidityController = HumidityController(servo=airChannelServo)
humidityController.startThread() # threaded because of DHT11 measurement
# humidity controller runs in the background

# main loop
while True:
    try:
        mixerController.mainLoop()
    except KeyboardInterrupt:
        running = False # exit thread
        exit()
        