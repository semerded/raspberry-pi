import gFrame
from src.pages.menu import Menu
from src.pages.game import Game
from src.pages.highscore import HighScore
from src.pages.enterName import EnterName
import src.data as data
import src.scoreHandler as scoreHandler

data.app = gFrame.AppConstructor(500, 500)

scoreHandler.loadHighScores()

PAGE_LISTING = [Menu(), Game(), HighScore(), EnterName()]

while True:
    data.app.eventHandler(fps=30)
    
    data.app.fill(gFrame.Color.DARKMODE)
    
    PAGE_LISTING[data.currentPage.value].place()
    
    
