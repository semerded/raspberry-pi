import gFrame
import src.data as data
from src.widgets.menuButton import MenuButton
from src.io import io_loop, io_mock
from time import time
from threading import Thread
from src.scoreHandler import addToHighScores


class Game:
    titleText = gFrame.Text(
        "Start The Game By Touching The Start Plate", gFrame.Font.H1, gFrame.Color.WHITE)
    titleTextRect = gFrame.Rect(0, 0, 500, 100)

    timerText = gFrame.Text("0.0", gFrame.Font.FONT100, gFrame.Color.WHITE)
    timerTextRect = gFrame.Rect(0, 100, 500, 300)

    penaltyText = gFrame.Text("0", gFrame.Font.LARGE, gFrame.Color.REDWOOD)

    def __init__(self) -> None:
        self.scoreWritten = False
        self.menuButton = MenuButton()

    def place(self):
        if not self.scoreWritten and data.gameState == data.gameStates.ended:
            self.scoreWritten = True
            addToHighScores(self.calculateTotalTime())
        
        if not data.ioActive:
            data.ioActive = True
            self.scoreWritten = False

            Thread(target=self.io_thread).start()

        if self.menuButton.checkInteractions():
            data.ioActive = False
            
        if time() - data.endGameTimer > data.END_GAME_INTERVAL and data.gameState == data.gameStates.ended:
            data.ioActive = False
            self.scoreWritten = False
            data.currentPage = data.pages.menu

        if data.gameState == data.gameStates.active:
            self.titleText.setText("Game Is Active")
            
        

        if data.app.drawElements():
            self.menuButton.place()

            self.titleText.placeInRect(self.titleTextRect)

            if data.gameState == data.gameStates.active:
                self.timerText.placeInRect(
                    self.timerTextRect, newText=self.calculateTime().__str__())
                self.penaltyText.setText(f"penalties: {data.penalties}")
                self.penaltyText.place(20, 400)
                
            elif data.gameState == data.gameStates.ended:
                self.titleText.setText("Game Has Ended")
                self.timerText.placeInRect(self.timerTextRect, newText=self.calculateTotalTime().__str__())

    def calculateTime(self):
        return round(time() - data.gameStartTime, 3)

    def calculateTotalTime(self):
        return round(time() - data.gameStartTime, 3) + (data.penalties * 5)
        
    def io_thread(self):
        while data.ioActive:
            # io_loop()
            io_mock()
