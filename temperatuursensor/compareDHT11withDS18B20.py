import time, Adafruit_DHT, logging
from w1thermsensor import W1ThermSensor
from gpiozero import LED

logging.basicConfig(filename="temperatureComparator.log",
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    filemode='w',
                    level=logging.INFO)
temperatureLogger = logging.getLogger()


DS18B20 = W1ThermSensor()
warningLed = LED(26)
previousTime = DHTfailedToReadCounter = 0
warningLedWarningMessage = "temperatuurverschil is hoger dan 2!"

while True:
    currentTime = time.time()

    if currentTime - previousTime > 2:  # 2 sec
        if DHTfailedToReadCounter > 10:
            temperatureLogger.error("DHT11 failed to read more than 10 times")
            DHTfailedToReadCounter = 0
            
        unused_humidity, DHTtemperature = Adafruit_DHT.read(Adafruit_DHT.DHT11, 5)
        DS18B20temperature = DS18B20.get_temperature()
        
        if DHTtemperature == None or DS18B20temperature == None:
            DHTfailedToReadCounter += 1
            continue
        DHTfailedToReadCounter = 0
        differenceBetweenSensors = abs(DS18B20temperature - DHTtemperature)
        
        print("temperatuur DHT11: %s°C" % DHTtemperature)
        print("temperatuur DS18B20: %s°C" % DS18B20temperature)
        print("verschil: %s°C" % differenceBetweenSensors)
        temperatureLogger.info(f"DHT11: {DHTtemperature} | DS18B20: {DS18B20temperature} | verschil: {differenceBetweenSensors}")
        
        if (differenceBetweenSensors > 2):
            warningLed.on()
            print("-" * len(warningLedWarningMessage))
            print(warningLedWarningMessage)
            print("-" * len(warningLedWarningMessage))
            temperatureLogger.warning(warningLedWarningMessage)
        else:
            warningLed.off()
        print() # print een enter
        previousTime = currentTime
