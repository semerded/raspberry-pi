from time import sleep
from gpiozero import LED

led = LED(23)
led2 = LED(24)

while True:
    led.on()
    led2.off()
    sleep(0.5)
    led.off()
    led2.on()
    sleep(0.5)
