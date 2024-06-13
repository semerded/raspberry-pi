import gFrame
from enum import Enum
import os

if os.path.isfile("highscores.json"):
    HIGHSCORES_PATH = "highscores.json"
else:
    HIGHSCORES_PATH = "zenuw_spiraal/highscores.json"

app: gFrame.AppConstructor = None


ioActive = False

class gameStates(Enum):
    notStarted = 0
    active = 1
    ended = 2

gameState = gameStates.notStarted
gameStartTime = 0
penalties = 0

highscores = {}

currentUser = None

endGame = False
endGameTimer = 0
END_GAME_INTERVAL = 5 # 5 sec


class pages(Enum):
    menu = 0
    game = 1
    highscore = 2
    enterName = 3
    
currentPage = pages.menu