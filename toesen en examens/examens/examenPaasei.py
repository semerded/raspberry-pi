from gpiozero import Button, AngularServo, PWMOutputDevice
import spidev, Adafruit_DHT, time
from threading import Thread

running = True

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


    
class DHT11:
    def __init__(self) -> None:
        self.humidity: float = 0
        self.temperature: float = 0

    def getTemperatureAndHumidity(self):
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

class MixerController():
    def __init__(self, motorPin: int, increaseSpeed: RpiButton, decreaseSpeed: RpiButton, confirm: RpiButton):
        self.mixMotor = PWMOutputDevice(motorPin)
        self.increaseSpeedButton = increaseSpeed
        self.decreaseSpeedButton = decreaseSpeed
        self.confirmSpeedButton = confirm
        self.currentSpeedStep = 1
        self.currentSpeed = 0
        
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
            self.mixMotor.value = (self.currentSpeedStep - 1) * 0.25
            print("motorsnelheid is succesvol geupdate")
            
            
class HumidityController(DHT11):
    airChannelAngleMapping = {100: 170, 90: 135, 75: 90,  60: 45, 40: 10} # humidity level: angle of airchannel
    def __init__(self, servo: AngularServo) -> None:
        super().__init__()
        self.servo = servo

    def startThread(self): # threaded
        Thread(target=self._threadedMainLoop)
        
    def _threadedMainLoop(self):
        while running:
            self.mainLoop()
            
    def mainLoop(self):
        humidity = super().getHumidity()
        self.controlAirChannelWithHumidity(humidity)
        
    def controlAirChannelWithHumidity(self, humidity: float):
        for requiredHumidity, servoAngle in self.airChannelAngleMapping:
            if humidity >= requiredHumidity:
                self.servo.angle = servoAngle
                break
                # time.sleep(0.2)
                # self.servo.detach()
                
                
        

decreaseSpeedButton = RpiButton(5)
increaseSpeedButton = RpiButton(6)
confirmSpeedButton = RpiButton(7)

mixerController = MixerController(motorPin=12, increaseSpeed=increaseSpeedButton, decreaseSpeed=decreaseSpeedButton, confirm=confirmSpeedButton)

airChannelServo = AngularServo(17)

humidityController = HumidityController(airChannelServo)
humidityController.startThread() # threaded because of DHT11 measurement

while True:
    try:
        mixerController.mainLoop()
    except KeyboardInterrupt:
        running = False
        exit()