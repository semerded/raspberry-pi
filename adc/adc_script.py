import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

def readSPI(channel):
    adc = spi.xfer2([1, (8 + channel) << 4,0])
    return ((adc[1] & 3) <<8) + adc[2]
    
channelLDR = 0

while True:
    licht_intensiteit = readSPI(channelLDR)
    print(licht_intensiteit)
    time.sleep(5)