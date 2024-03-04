from gpiozero import Button, LED, AngularServo
import time

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
    

class DRScore:
    def __init__(self, servoPin: int, drsPin: int, brake: Button, indicationLedPin: int) -> None:
        self.servo = AngularServo(servoPin)
        self.servo.angle = 15
        self.servo.detach()
        self.drsButton = RpiButton(drsPin)
        self.brakeButton = brake
        self.indicationLed = LED(indicationLedPin)
        
        self.drsStatus = False
    
    def _setStatusByButton(self):
        if self.drsButton.isClicked():
            self.drsStatus = not self.drsStatus
            if self.drsStatus:
                self._openDrs()
            else:
                self._closeDrs()
            
    def _setStatusByBrake(self):
        if self.brakeButton.is_active:
            self.drsStatus = False
            self._closeDrs()
        
    def _openDrs(self):
        self.servo.angle = 75
        
    
    def _closeDrs(self):
        self.servo.angle = 15
        
    def updateIndicationLed(self):
        if self.drsStatus:
            self.indicationLed.on()
        else:
            self.indicationLed.off()
        
    def DRScontrol(self):
        self._setStatusByButton()
        self._setStatusByBrake()
        self.updateIndicationLed()
        print(self.servo.value)
        time.sleep(0.1)
        self.servo.detach()
        
class DRS(DRScore):
    def __init__(self, servoPin: int, drsPin: int, brake: Button, indicationLedPin: int) -> None:
        super().__init__(servoPin, drsPin, brake, indicationLedPin)
        self.active = False
        self.deActivating = False
        self.buttonClickedAt = 0
        
        self.START_TIME = 1.765 # TODO change names
        self.STOP_TIME = 1.876
        
    def DRScontrol(self):
        if self.active:
            super().DRScontrol()
            self.deActivationSequence()
        else:
            self.activationSequence()
        
    def activationSequence(self):
        if self.drsButton.is_held and not self.deActivating:
            if self.drsButton.held_time > self.START_TIME:
                self.active = True
    
    def deActivationSequence(self):
        if self.drsButton.is_held:
            if self.drsButton.held_time > self.STOP_TIME:
                self.active = False
            
    

        

brake = Button(3)
drsSystem = DRS(17, 2, brake, 4)

while True:
    drsSystem.DRScontrol()
    
