import time, logging, Adafruit_DHT
from gpiozero import LED, Button
from enum import Enum

LOGGING_FILE_LOCATION = "coolRoom.log"



logging.basicConfig(filename=LOGGING_FILE_LOCATION,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    filemode='w',
                    level=logging.INFO)
logger = logging.getLogger()


class ...(Enum):
    ...

class ...:
    def __init__(self) -> None:
        pass
    
    
while True:
    ...