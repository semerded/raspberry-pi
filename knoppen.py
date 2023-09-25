from gpiozero import LED, Button
from time import sleep

led1 = LED(10)
led2 = LED(11)
setButton = Button(8, pull_up=False)
previousSetButton = False
resetButton = Button(9)
previousResetButton = False
counter = 0


while True:
    
    if setButton.is_active != previousSetButton:
        if setButton.is_active:
            counter += 1
        previousSetButton = setButton.is_active
    if resetButton.is_active != previousResetButton:
        if resetButton.is_active:
            counter = 0
        previousResetButton = resetButton.is_active
    
    
    print(counter)
    led1.off()
    led2.off()
    if counter != 0:
        if counter % 3 ==  1:
            led1.on()
        elif counter % 3 == 2:
            led2.on()
        elif counter % 3 == 0:
            led1.on()
            led2.on()
        
    