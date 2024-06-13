import gFrame
import src.data as data
from src.widgets.menuButton import MenuButton

class HighScore:
    highScoreText = gFrame.Text("HighScores", gFrame.Font.XXLARGE, gFrame.Color.WHITE)
    
    def __init__(self) -> None:
        self.menuButton = MenuButton()
        
        self.highscoreTextList = []
        for _ in range(10):
            indexText = gFrame.Text("name", gFrame.Font.LARGE, gFrame.Color.WHITE)
            timeText = gFrame.Text("0", gFrame.Font.LARGE, gFrame.Color.WHITE)
            
            timeSegment = [indexText, timeText]
            self.highscoreTextList.append(timeSegment)
        
    def place(self):
        self.menuButton.checkInteractions()
        
        if data.app.drawElements():
            self.menuButton.place()
            
            self.highScoreText.placeInRect(gFrame.Rect(0, 0, 500, 70), )
            
            for index, (name, time) in enumerate(data.highscores.items()):
                if index > len(data.highscores) - 1:
                    break
                
                indexText = self.highscoreTextList[index][0]
                indexRect = gFrame.Rect(100, 90 + (index * 40), 150, 40)
                timeText = self.highscoreTextList[index][1]
                timeRect = gFrame.Rect(250, 90 + (index * 40), 150, 40)
                
                indexText.placeInRect(indexRect, newText=name)
                timeText.placeInRect(timeRect, newText=time.__str__())
            
                gFrame.Draw.borderFromRect(indexRect, 1, gFrame.Color.COFFEE)
                gFrame.Draw.borderFromRect(timeRect, 1, gFrame.Color.COFFEE)

                