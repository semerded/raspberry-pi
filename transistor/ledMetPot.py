import RPi.GPIO as IO, spidev, time

IO.setmode(IO.BCM)
IO.setwarnings(False)
IO.setup(12, IO.OUT)
pwm = IO.PWM(12, 100)
pwm.start(0)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

def readSPI(channel):
    adc = spi.xfer2([1, (8 + channel) << 4,0])
    return ((adc[1] & 3) <<8) + adc[2]

potChannel = 0

while True:
    potWaarde = readSPI(potChannel)
    print(potWaarde)
    potWaarde /= 10.23
    pwm.ChangeDutyCycle(potWaarde)
    time.sleep(0.1)