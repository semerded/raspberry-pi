import json
import src.data as data

def loadHighScores():
    with open(data.HIGHSCORES_PATH) as fp:
        data.highscores = json.load(fp)

def updateHighScores():        
    with open(data.HIGHSCORES_PATH, "w") as fp:
        json.dump(data.highscores, fp)
        
def scorePosition(score):
    for index, _score in enumerate(data.highscores.values()):
        if score < _score:
            return index
    return len(data.highscores)
        
def addToHighScores(score: float):
    data.highscores[data.currentUser] = score
    dict(sorted(data.highscores.items(), key=lambda item: item[1]))
    updateHighScores()
    loadHighScores()