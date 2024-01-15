import spidev, time, logging

LOGGING_FILE_LOCATION = "adc.log"

logging.basicConfig(filename=LOGGING_FILE_LOCATION,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    filemode='a',
                    level=logging.INFO)
adcLogger = logging.getLogger()

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

def readSPI(channel):
    adc = spi.xfer2([1, (8 + channel) << 4,0])
    return ((adc[1] & 3) <<8) + adc[2]
    
channelLDR1 = 0
channelLDR2 = 1

while True:
    lightSensor1 = readSPI(channelLDR1)
    lightSensor2 = readSPI(channelLDR2)
    averageLightValue = (lightSensor1 + lightSensor2) / 2
    adcLogger.info(averageLightValue)
    print("data succesfully logged")
    time.sleep(5)