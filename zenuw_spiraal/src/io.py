from gpiozero import Button
import src.data as data
from time import time, sleep
import gFrame, pygame

# button


class ButtonExtended(Button):
    """
    remake om de `isClicked` functie toe te voegen
    """

    def __init__(self, pin=None, pull_up=True, active_state=None, bounce_time=None, hold_time=1, hold_repeat=False, pin_factory=None):
        super().__init__(pin, pull_up, active_state,
                         bounce_time, hold_time, hold_repeat, pin_factory)
        self.alreadyClicked = False

    def isClicked(self):
        if self.is_active:
            if not self.alreadyClicked:
                self.alreadyClicked = True
                return True
        else:
            self.alreadyClicked = False
        return False


# START = ButtonExtended(4)
# STOP = ButtonExtended(5)
# SPIRAL_TOUCH = ButtonExtended(6)


cheatPenaltyTimer = 0
CHEAT_PENALTY_TIMER_INTERVAL = 1


def io_loop():
    global cheatPenaltyTimer

    if START.is_active and data.gameState == data.gameStates.notStarted:
        data.gameState = data.gameStates.active
        data.gameStartTime = time()

    if STOP.is_active and data.gameState == data.gameStates.active:
        data.gameState = data.gameStates.ended
        data.endGameTimer = time()

    if SPIRAL_TOUCH.isClicked() and data.gameState == data.gameStates.active:
        data.penalties += 1
        cheatPenaltyTimer = time()

    if SPIRAL_TOUCH.is_active and time() - cheatPenaltyTimer > CHEAT_PENALTY_TIMER_INTERVAL and data.gameState == data.gameStates.active:
        data.penalties += 5

    sleep(1/1000)
    
    
def io_mock():
    global cheatPenaltyTimer
    
    # print(data.gameState)

    if gFrame.Interactions.isKeyPressing(pygame.K_a) and data.gameState == data.gameStates.notStarted:
        
        data.gameState = data.gameStates.active
        data.gameStartTime = time()

    if gFrame.Interactions.isKeyPressing(pygame.K_z) and data.gameState == data.gameStates.active:
        data.gameState = data.gameStates.ended
        data.endGameTimer = time()
        

    if gFrame.Interactions.isKeyClicked(pygame.K_e) and data.gameState == data.gameStates.active:
        data.penalties += 1
        cheatPenaltyTimer = time()

    if gFrame.Interactions.isKeyPressing(pygame.K_e) and time() - cheatPenaltyTimer > CHEAT_PENALTY_TIMER_INTERVAL and data.gameState == data.gameStates.active:
        data.penalties += 5
        cheatPenaltyTimer = time()
        
    sleep(1/30) # sync clock
