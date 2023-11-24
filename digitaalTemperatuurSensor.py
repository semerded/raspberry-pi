import time
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()

while True:
    temperatuur = sensor.get_temperature()
    print("De temperatuur in graden Celsius is nu ", temperatuur)
    time.sleep(1)
    