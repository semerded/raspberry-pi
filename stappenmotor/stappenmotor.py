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
# potmeter
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
        return self.readADC(self.potmeterChannel)
    
    
    
#stepper motor
class StepperMotor:
    def __init__(self, stepperMotor: RpiMotorLib.BYJMotor) -> None:
        self.stepperMotor = stepperMotor
        self.GPIO_PINS = [18, 23, 24, 25]
        self.REVOLUTION_STEP_NUMBER = 512
        self.active = False
        self.stepsDone = 0
        self.speed = 0.001



    def rotateBySteps(self, steps: int, direction: stepperDirection):
        self.active = True
        if isinstance(direction, stepperDirection):
            self._rotateMotorBySteps(steps, direction.value)
        else:
            self._rotateMotorBySteps(steps, direction)     

    
    def _rotateMotorBySteps(self, steps: int, direction):
        for step in range(steps):
            self.stepperMotor.motor_run(self.GPIO_PINS, steps=1, ccwise=direction, wait=self.speed, initdelay=0)
            self.stepsDone += 1
            if not self.isActive():
                return False
        self.active = False
        return True
            # self.remainingSteps TODO add remaining steps
        
    def stop(self):
        self.stepperMotor.motor_stop()
        
    def isActive(self):
        return self.active
    
        
class StepperMotorInputControl(StepperMotor):
    def __init__(self, stepperMotor: RpiMotorLib.BYJMotor, startButton: Button, stopButton: Button, potmeter: StepperMotorSpeedControl) -> None:
        super().__init__(stepperMotor)
        self.potmeter = potmeter
        self.startButton = startButton
        self.stopButton = stopButton
        self.distancePerRevolution = 1 # mm
        
    def setDistancePerRevolution(self, distancePerRevolution: float):
        self.distancePerRevolution = distancePerRevolution
        
    def rotateByDistance(self, distance: float, direction: stepperDirection):
        self.active = True
        distance = int((self.REVOLUTION_STEP_NUMBER / self.distancePerRevolution) * distance) - self.stepsDone
        self.stepsDone = 0
        Thread(target=self.rotateBySteps, args=(distance, direction)).start()
        while self.active:
            self.speed = 0.001 + self.potmeter.readValues() / 50000
            print(self.speed)
            if stopButton.is_active:
                print(False)
                self.active = False
                
    def activate(self, distance: float, direction: stepperDirection):
        while True:
            if not self.isActive() and self.stopButton.is_active: # knop blijft geactiveerd uit vorige script
                return
            if self.startButton.is_active:
                if self.rotateByDistance(distance, direction):
                    return 
                
            

    
    
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
potmeter = StepperMotorSpeedControl(0)
    

stepperMotor = RpiMotorLib.BYJMotor("stepperMotor")
stepperMotorController = StepperMotorInputControl(stepperMotor, startButton, stopButton, potmeter)
stepperMotorController.setDistancePerRevolution(6)

def resetVariables():
    global reverseMotor
    reverseMotor = False
    
while True:
    resetVariables()
    distance = intput("geef de afstand in milimeter op (negatief om terug te draaien): ")
    if distance < 0:
        reverseMotor = True

    stepperMotorController.activate(distance, reverseMotor)
