import spidev, time, logging, RPI.GPIO as IO


class ADCreader:
    def __init__(self) -> None:
        self.spi = spidev.Spidev()
        self.spi.open(0, 0)
        self.max_speed_hz = 1000000
    
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
            self.pinListing[pin] = IO.PWM(pin, 255)
            self.pinListing[pin].start(0)
            
    def setPWMvalue(self, pin: int, value: int):
          self.pinListing[pin].ChangeDutyCycle(value)
  
        
class Motor(PWM):
    def __init__(self, motorPin) -> None:
        self.pin = motorPin
        super().__init__(motorPin)
        
    def setSpeed(self, speed: int):
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
        self._mapTempToSpeed(adcValue)
        self.setSpeed(adcValue)
        
    def _mapTempToSpeed(self, tempValue):
        pass


# temperatureReactiveMotor = TemperatureReactiveMotor(12, 0, 10, 30)
reader = ADCreader()


while True:
    reader.readADC(0)
    # temperatureReactiveMotor.activate()
    