import time
import RPi.GPIO as IO
from gpiozero import Button, AngularServo
import bme280
from threading import Thread
import smbus2

"""
2 threades
    -> main thread om knoppen te besturen
    -> 2de thread om bme280 uit te meten
"""
    
active = True

###########################
# bme280 with servo setup #
###########################

SERVO_PIN = 10

BME280_PORTS = (1, 2)
BME280_ADRESS = (0x76, 0x77)
bus1 = smbus2.SMBus(BME280_PORTS[0])
bus2 = smbus2.SMBus(BME280_PORTS[1])
calibration_params1 = bme280.load_calibration_params(bus1, BME280_ADRESS[0])
calibration_params2 = bme280.load_calibration_params(bus2, BME280_ADRESS[1])
    
def readBME280s():
    bme280data1 = bme280.sample(bus1, BME280_ADRESS[0], calibration_params1)
    bme280data2 = bme280.sample(bus2, BME280_ADRESS[1], calibration_params2)
    temperature1 = bme280data1.temperature
    temperature2 = bme280data2.temperature
    return list(temperature1, temperature2)


def ThreadedTemperatureControl():
    # variables worden gedefinieerd in functie omdat ze hier ook enkel gebruikt worden
    temperature = None
    previousTemperature = None
    previousTemperatureMeasurement = 0
    currentTemperatureMeasurement = time.time()
    TEMPERATURE_MEASUREMENT_INTERVAL = 1
    
    servoParameters = {65: 180, 55: 150, 45: 120, 35: 90, 25: 60, 15: 30, "default": 0}
    
    servo = AngularServo(SERVO_PIN)
    servo.angle = 0
    
    while active: # Thread loop
        currentTemperatureMeasurement = time.time()
        
        if previousTemperature != temperature:
            previousTemperature = temperature
            for parameter, angle in servoParameters:
                if parameter == "default": # servo is 0 graden bij een temperatuur kleiner dan 15°C
                    servo.angle = angle
                    break
                if temperature > parameter:
                    servo.angle = angle
                    break
        
        if currentTemperatureMeasurement - previousTemperatureMeasurement >= TEMPERATURE_MEASUREMENT_INTERVAL:
            _temperature = readBME280s()
            try: # zorgt ervoor dat als de sensor een foute waarde terug geeft de code niet crasht
                temperature = sum(_temperature) / len(_temperature) # berekent het gemiddelde
            except:
                pass
            

#################################
# drukknoppen met rgb led setup #
#################################


BUTTON_PRESS_INTERVAL: float = 1.7

RGB_IO_PINS = (11, 12, 13)
RGB_PWM_PINS = []

BUTTON_IO_PINS = (14, 15, 16)
BUTTONS = [Button(BUTTON_IO_PINS[0]), Button(BUTTON_IO_PINS[1]), Button(BUTTON_IO_PINS[2])]
buttonsActive = [0, 0, 0]

for index, pin in enumerate(RGB_IO_PINS): # RGB PWM setup
    IO.setup(pin, IO.OUT)
    RGB_PWM_PINS.append(IO.PWM(pin, 100))
    RGB_PWM_PINS[index].start(0)
    
    
def setRGB_LED_Color(r: int, g: int, b: int):
    # PWM werkte best van 0 tot 100
    RGB_PWM_PINS[0].ChangeDutyCycle(r / 2.55)
    RGB_PWM_PINS[1].ChangeDutyCycle(g / 2.55)
    RGB_PWM_PINS[2].ChangeDutyCycle(b / 2.55)



RGB_LED_COLOR_LISTING: dict[list[bool], tuple[int]] = {
    (True, False, False): (255, 0, 0),
    (False, True, False): (255, 130, 0),
    (False, False, True): (255, 255, 0),
    (True, True, False): (0, 255, 0),
    (False, True, True): (0, 0, 255),
    (True, False, True): (255, 0, 255)
}

def checkHeldTimeThreshold(button: Button):
    if button.held_time != None:
        return button.held_time  >= BUTTON_PRESS_INTERVAL
    return False



if __name__ == "__main__":
    Thread(target=ThreadedTemperatureControl).start()
    
    try:
        while True: # main thread    
            try:     
                if checkHeldTimeThreshold(BUTTONS[0]) or checkHeldTimeThreshold(BUTTONS[1]) or checkHeldTimeThreshold(BUTTONS[2]):
                    for index, button in enumerate(BUTTONS):
                        buttonsActive[index] = button.is_active
                        
                    buttonsActive = tuple(buttonsActive)
                    if buttonsActive in RGB_LED_COLOR_LISTING.keys():
                        setRGB_LED_Color(*RGB_LED_COLOR_LISTING[buttonsActive])
            except TypeError:
                pass # held time geeft None terug als hij niet is ingedrukt
    except KeyboardInterrupt:
        active = False
        exit(130)
    
    except Exception as e:
        active = False
        print(e.with_traceback())
        exit(1)

            