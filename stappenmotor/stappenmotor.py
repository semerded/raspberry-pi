from RpiMotorLib import RpiMotorLib
from gpiozero import Button
from enum import Enum
from threading import Thread
import spidev

#* enums
class stepperDirection(Enum):
    left = True
    right = False

#* classes
class ADCreader:
    def __init__(self) -> None:
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1000000
    
    def readADC(self, channel: int):
        adc = self.spi.xfer2([1, (8 + channel) << 4,0])
        return ((adc[1] & 3) <<8) + adc[2]

class StepperMotorSpeedControl(ADCreader):
    def __init__(self, potmeterChannel: int) -> None:
        super().__init__()
        self.potmeterChannel = potmeterChannel
    
    def readValues(self):
        adcSignal = self.readADC(self.potmeterChannel)
    
class StepperMotor:
    def __init__(self, stepperMotor: RpiMotorLib.BYJMotor) -> None:
        self.stepperMotor = stepperMotor
        self.GPIO_PINS = [18, 23, 24, 25]
        self.REVOLUTION_STEP_NUMBER = 2048
        self.active = False
        self.remainingSteps: int


    def rotateBySteps(self, steps: int, direction: stepperDirection):
        self.active = True
        self.remainingSteps = steps
        if isinstance(direction, stepperDirection):
            self._rotateMotorBySteps(steps, direction.value)
        else:
            self._rotateMotorBySteps(steps, direction)     

        self.active = False
    
    def _rotateMotorBySteps(self, steps: int, direction):
        for step in range(self.remainingSteps):
            self.stepperMotor.motor_run(self.GPIO_PINS, steps=1, ccwise=direction, steptype="full")
            # self.remainingSteps TODO add remaining steps
        
    def stop(self):
        self.stepperMotor.motor_stop()
        
    def isActive(self):
        return self.active
        
class StepperMotorInputControl(StepperMotor):
    def __init__(self, stepperMotor: RpiMotorLib.BYJMotor, stopButton: Button, potmeter: StepperMotorSpeedControl) -> None:
        super().__init__(stepperMotor)
        self.potmeter = potmeter
        self.stopButton = stopButton
        self.distancePerRevolution = 1 # mm 
        self.speed = 0.001
        
    def setDistancePerRevolution(self, distancePerRevolution: float):
        self.distancePerRevolution = distancePerRevolution
        
    def rotateByDistance(self, distance: float, direction: stepperDirection):
        distance = int((self.REVOLUTION_STEP_NUMBER / self.distancePerRevolution) * distance)
        Thread(target=self.rotateBySteps, args=(distance, direction))
        while self.active:
            self.speed = self.potmeter.readValues() / 10000
            if stopButton.is_active:
                self.active = False

    
    
def intput(message: object = "", wrongInputMessage: str = "Input must be an int or float") -> float:
    """
    gives an input prompt and tries to convert it to an number (float), on succes the input will be converted and returned. 
    """
    while True:
        prompt = input(message)
        try:
            return float(prompt)
        except ValueError:
            print(wrongInputMessage)
            
        
    
    
startButton = Button(5)
stopButton = Button(6)
potmeter = StepperMotorSpeedControl()
    

stepperMotor = RpiMotorLib.BYJMotor("stepperMotor")
stepperMotorController = StepperMotorInputControl(stepperMotor, startButton, stopButton)
stepperMotorController.setDistancePerRevolution(6)

def resetVariables():
    global reverseMotor
    reverseMotor = False
    


while True:
    resetVariables()
    distance = intput("geef de afstand in milimeter op (negatief om terug te draaien): ")
    
    if distance < 0:
        reverseMotor = True
    
    if startButton.is_active:
        stepperMotorController.rotateByDistance(distance, reverseMotor)
        
    
        





    