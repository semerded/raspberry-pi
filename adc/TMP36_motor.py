import spidev, RPi.GPIO as IO

class ADCreader:
    def __init__(self) -> None:
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1000000
    
    def readADC(self, channel: int):
        adc = self.spi.xfer2([1, (8 + channel) << 4,0])
        return ((adc[1] & 3) <<8) + adc[2]
    
    
class PWM:
    def __init__(self, *PWMpins) -> None:
        IO.setmode(IO.BCM)
        IO.setwarnings(False)
        self.pinListing = {}
        self._IOsetup(PWMpins)
        
    def _IOsetup(self, PWMpins):
        for pin in PWMpins:
            IO.setup(pin, IO.OUT)
            self.pinListing[pin] = IO.PWM(pin, 100)
            self.pinListing[pin].start(0)
            
    def setPWMvalue(self, pin: int, value: int):
        if value >= 0 and value <= 100:
          self.pinListing[pin].ChangeDutyCycle(value)
  
        
class Motor(PWM):
    def __init__(self, motorPin) -> None:
        self.pin = motorPin
        super().__init__(motorPin)
        
    def setSpeed(self, speed: int):
        print(speed)
        self.setPWMvalue(self.pin, speed)
        
        
class TemperatureReactiveMotor(Motor):
    def __init__(self, motorPin: int, ADCchannel: int, minTemp: float, maxTemp: float) -> None:
        super().__init__(motorPin)
        self.adcReader = ADCreader()
        self.adcChannel = ADCchannel
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        
    def activate(self):
        adcValue = self.adcReader.readADC(self.adcChannel)
        self.setSpeed(self._mapTempToSpeed(adcValue))   
  
    def _mapTempToSpeed(self, adcValue):
        temperature = (((adcValue * 3.3) / 1024) - 0.5) * 100
        return self.overwriteMotorSpeed(temperature)
        
    def overwriteMotorSpeed(self, speed):
        return (speed - self.minTemp) / (self.maxTemp - self.minTemp) * 100     


temperatureReactiveMotor = TemperatureReactiveMotor(12, 0, 10, 30)

while True:
    temperatureReactiveMotor.activate()
    