from time import sleep
from gpiozero import LED

varLed = LED(18)

while True:
    varLed.on()
    sleep(0.5)
    varLed.off()
    sleep(0.5)
