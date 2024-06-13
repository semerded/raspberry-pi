import gFrame
import src.data as data
import sys
import os


class Menu:
    if os.path.isfile("src/assets/Exquisite Corpse.ttf"):
        fontPath = "src/assets/Exquisite Corpse.ttf"
    else:
        fontPath = "zenuw_spiraal/src/assets/Exquisite Corpse.ttf"
    font = gFrame.Font.customFont(50, fontPath)
    titleText = gFrame.Text("De Zenuw Spiraal", font, gFrame.Color.REDWOOD)
    titleText.setHover(30)
    
    # subTitleText = gFrame.Text("Durf jij het aan?")
    
    startGameButton = gFrame.Button((250, 50), gFrame.Color.COFFEE, 3)
    startGameButton.setBorder(3, gFrame.Color.WHITE)
    startGameButton.text("start", gFrame.Font.MEDIUM, gFrame.Color.WHITE)

    highScoreButton = gFrame.Button((250, 50), gFrame.Color.COFFEE, 3)
    highScoreButton.setBorder(3, gFrame.Color.WHITE)
    highScoreButton.text("highscores", gFrame.Font.MEDIUM, gFrame.Color.WHITE)

    quitButton = gFrame.Button((250, 50), gFrame.Color.COFFEE, 3)
    quitButton.setBorder(3, gFrame.Color.WHITE)
    quitButton.text("quit", gFrame.Font.MEDIUM, gFrame.Color.WHITE)

    def __init__(self) -> None:
        pass

    def place(self):
        if self.startGameButton.isClicked():
            data.currentPage = data.pages.enterName
            data.gameState = data.gameStates.notStarted

        if self.highScoreButton.isClicked():
            data.currentPage = data.pages.highscore

        if self.quitButton.isClicked():
            sys.exit()

        if data.app.drawElements():
            self.titleText.place(250 - self.titleText.getRect.width / 2, 50)
            
            self.startGameButton.place(125, 320)

            self.highScoreButton.place(125, 380)

            self.quitButton.place(125, 440)
