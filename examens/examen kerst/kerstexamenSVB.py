import time, logging, Adafruit_DHT
from gpiozero import LED, Button
from enum import Enum

LOGGING_FILE_LOCATION = "coolRoom.log"

DHT_PIN = 4

Adafruit_DHT.read(Adafruit_DHT.DHT11, DHT_PIN)

logging.basicConfig(filename=LOGGING_FILE_LOCATION,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    filemode='w',
                    level=logging.INFO)
logger = logging.getLogger()

previousTime = 0
waitTime = 1
if time.time() - previousTime >= waitTime:
    ...

class ...(Enum):
    ...

class ...:
    def __init__(self) -> None:
        pass
    
    
while True:
    ...
    
    

REDLIGHT = [LED(10), LED(11), LED(12)] # red, yellow, green
