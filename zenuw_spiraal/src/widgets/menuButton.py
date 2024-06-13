import gFrame
import src.data as data
import os

class MenuButton:
    def __init__(self) -> None:
        self.button = gFrame.Button((30, 30), gFrame.Color.DARKMODE)
        if os.path.isfile("src/icons/menu.png"):
            path = "src/icons/menu.png"
        else:
            path = "zenuw_spiraal/src/icons/menu.png"
        self.button.icon(path)
        
    def checkInteractions(self):
        if self.button.isClicked():
            data.currentPage = data.pages.menu
            data.gameState = False
            return True
        return False
    
    def place(self):
        self.button.place(460, 10)