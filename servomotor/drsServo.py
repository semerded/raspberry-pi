from gpiozero import Button, LED, Servo

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
        self.servo = Servo(servoPin)
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
        self.servo.max()
    
    def _closeDrs(self):
        self.servo.close()
        
    def updateIndicationLed(self):
        self.indicationLed = self.drsStatus 
        
    def DRScontrol(self):
        self._setStatusByButton()
        self._setStatusByBrake()
        self.updateIndicationLed()
        

brake = Button(3)
drsSystem = DRScore(17, 2, brake, 4)

while True:
    drsSystem.DRScontrol()
    
