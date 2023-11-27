import time
import Adafruit_DHT
import logging
from w1thermsensor import W1ThermSensor
from gpiozero import LED


class WarningLed:
    def __init__(self, ledPin: int, ledBlinkSpeedMs: int = 200) -> None:
        self.ledPin = ledPin
        self.ledBlinkSpeed = ledBlinkSpeedMs / 2  # half time on, half time off
        self.previousTime = 0
        self.ledOn = False

    def ledBlink(self):
        self.currentTime = time.time
        if self.currentTime - self.previousTime > self.ledBlinkSpeed:
            self.ledOn = not self.ledOn
            if self.ledOn:
                LED(self.ledPin).on()
            else:
                self.ledOff()

    def ledOff(self):
        LED(self.ledPin).off()

    def warningLedController(self):
        if self.ledBlinkStatus:
            self.ledBlink()
        else:
            self.ledOff()

    @property.setter
    def setWarningLed(self, status: bool):
        self.ledBlinkStatus = status


logging.basicConfig(filename="temperatureComparator.log",
                    format='%(asctime)s %(message)s',
                    filemode='w',
                    level=logging.INFO)
temperatureLogger = logging.getLogger()


DS18B20 = W1ThermSensor()
warningLed = WarningLed()
previousTime = 0

while True:
    currentTime = time.time
    warningLed.warningLedController()

    if currentTime - previousTime > 2000:  # 2 sec
        unused_humidity, DHTtemperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4, 2)
        DS18B20temperature = DS18B20.get_temperature()

        differenceBetweenSensors = abs(DS18B20temperature - DHTtemperature)
        if (differenceBetweenSensors > 2):
            warningLed.setWarningLed(True)
        else:
            warningLed.setWarningLed(False)

        print("temperatuur DHT11: %s°C" % DHTtemperature)
        print("temperatuur DS18B20: %s°C" % DS18B20temperature)
        print("verschil: %s°C" % differenceBetweenSensors)
        temperatureLogger.info(f"DHT11: {DHTtemperature} | DS18B20: {DS18B20temperature} | verschil: {differenceBetweenSensors}")
        previousTime = currentTime
