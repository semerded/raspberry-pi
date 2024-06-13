import gFrame
import src.data as data
from src.widgets.menuButton import MenuButton
import pygame_textinput
import string




class EnterName:
    titleText = gFrame.Text("Enter Your Unique Name (max 10 char)", gFrame.Font.LARGE, gFrame.Color.REDWOOD)
    titleTextRect = gFrame.Rect(0, 0, 500, 100)
    
    textInputBackground = gFrame.Rect(10, 200, 480, 50)
    
    confirmButton = gFrame.Button((250, 100), gFrame.Color.REDWOOD, 5)
    confirmButton.setBorder(5, gFrame.Color.WHITE)
    confirmButton.text("Confirm Name", gFrame.Font.XLARGE, gFrame.Color.WHITE)
    
    validCharacters = string.ascii_letters + string.digits + " _-."
    
    
    def __init__(self) -> None:
        self.menuButton = MenuButton()
        self.textInput = pygame_textinput.TextInputVisualizer(font_color=gFrame.Color.WHITE)

    def place(self):
        self.menuButton.checkInteractions()
        
        self.textInput.update(data.app.getEvents)
        
        if self.checkInput():
            self.confirmButton.updateColor(gFrame.Color.GREEN)
        else:
            self.confirmButton.updateColor(gFrame.Color.REDWOOD)
        
        if self.confirmButton.isClicked() and self.checkInput():
            data.currentUser = self.textInput.value
            data.currentPage = data.pages.game

        if data.app.drawElements():
            self.menuButton.place()
            
            self.titleText.placeInRect(self.titleTextRect)
            
            gFrame.Draw.rectangleFromRect(self.textInputBackground, gFrame.Color.REDWOOD)
            gFrame.vars.mainDisplay.blit(self.textInput.surface, (20, 215))
            
            self.confirmButton.place(125, 350)
            
        
    def checkInput(self):
        userInput = self.textInput.value
        if len(userInput) <= 10 and len(userInput) >= 3:
            validWord = True
            for letter in userInput:
                if not letter in self.validCharacters:
                    validWord = False
            if validWord:
                if not userInput in data.highscores:
                    return True
        
        return False
