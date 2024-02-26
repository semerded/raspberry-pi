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
# button
class RpiButton(Button):
    """
    remake om de `isClicked` functie toe te voegen
    """
    def __init__(self, pin=None, pull_up=True, active_state=None, bounce_time=None, hold_time=1, hold_repeat=False, pin_factory=None):
        super().__init__(pin, pull_up, active_state, bounce_time, hold_time, hold_repeat, pin_factory)
        self.alreadyClicked = False
        
    def isClicked(self):
        if self.is_active:
            if not self.alreadyClicked:
                self.alreadyClicked = True
                return True
        else:
            self.alreadyClicked = False
        return False
        

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
        return 0.001 + self.readADC(self.potmeterChannel) / 50000
    
    
    
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

    
    def _rotateMotorBySteps(self, steps: int, direction: bool):
        for step in range(steps):
            self.stepperMotor.motor_run(self.GPIO_PINS, steps=1, ccwise=direction, wait=self.speed, initdelay=0)
            self.stepsDone += 1
            if not self.isActive():
                return False
        self.active = False
        return True
        
    def stop(self):
        self.stepperMotor.motor_stop()
        
    def isActive(self):
        return self.active
    
        
class StepperMotorInputControl(StepperMotor):
    def __init__(self, stepperMotor: RpiMotorLib.BYJMotor, startButton: RpiButton, stopButton: RpiButton, potmeter: StepperMotorSpeedControl) -> None:
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
        
        Thread(target=self.rotateBySteps, args=(distance, direction)).start()
        while self.active:
            self.speed = self.potmeter.readValues()
            if self.stopButton.isClicked():
                print("motor gepauseerd")
                self.active = False
                return False
        return True
                
    def activate(self, distance: float, direction: stepperDirection):
        self.stepsDone = 0

        while True:
            try:
                if not self.isActive() and self.stopButton.isClicked():
                    print("motor gestopt\n")
                    return
                if self.startButton.is_active:
                    if self.rotateByDistance(distance, direction):
                        print("motor klaar\n")
                        return 
            except KeyboardInterrupt:
                self.active = False # om de thread te stoppen
                exit()

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
            
        
#* init objects   
startButton = RpiButton(5)
stopButton = RpiButton(6)
potmeter = StepperMotorSpeedControl(0)
    
stepperMotor = RpiMotorLib.BYJMotor("stepperMotor")
stepperMotorController = StepperMotorInputControl(stepperMotor, startButton, stopButton, potmeter)
stepperMotorController.setDistancePerRevolution(6)


#* main   
while True:
    reverseMotor = False
    distance = intput("geef de afstand in milimeter op (negatief om terug te draaien): ")
    if distance < 0:
        reverseMotor = True
        distance = abs(distance)

    stepperMotorController.activate(distance, reverseMotor)
