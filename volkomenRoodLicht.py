from gpiozero import LED, LightSensor # import de componenten uit de library die je nodig hebt
from time import sleep # om delay's toe te voegen

# duid de pinnen aan van de verschillende componenten
AUTOROOD = LED(10)
AUTOGEEL = LED(9)
AUTOGROEN = LED(11)

FIETSROOD = LED(13)
FIETSGEEL = LED(19)
FIETSGROEN = LED(26)

LDR = LightSensor(21)

class stoplicht: # maak een class aan met de verschillende standen van het stoplicht
    def __init__(self, lichtRood, lichtGeel, lichtGroen) -> None: # maak de class aan en voeg de verschillende lichten toe
        self.__lichtRood = lichtRood
        self.__lichtGeel = lichtGeel
        self.__lichtGroen = lichtGroen
        
        
    def Rood(self): # lichtstand rood
        self.__lichtRood.on()
        self.__lichtGeel.off()
        self.__lichtGroen.off()
        
    
    def Geel(self): # lichtstand geel
        self.__lichtRood.off()
        self.__lichtGeel.on()
        self.__lichtGroen.off()

        
    def Groen(self): # lichtstand groen
        self.__lichtRood.off()
        self.__lichtGeel.off()
        self.__lichtGroen.on()       
    
fietsLicht = stoplicht(FIETSROOD, FIETSGEEL, FIETSGROEN) # voeg de standen van de class aan de fietslichten toe
autoLicht = stoplicht(AUTOROOD, AUTOGEEL, AUTOGROEN) # voeg de standen van de class aan de autolichten toe

tijdGeel = 1 # de tijd dat het geel is
tijdGroen = 5 # de tijd dat het groen/rood is

while True: # maak loop
    if LDR.is_active: # als de LDR licht detecteerd
        fietsLicht.Geel() # geel licht voor fietsers
        autoLicht.Geel() # geel licht voor auto's
        sleep(tijdGeel) # tijd dat het geel blijft
        fietsLicht.Groen()
        autoLicht.Rood()
        sleep(tijdGroen)
        fietsLicht.Geel()
        autoLicht.Geel()
        sleep(tijdGeel)
    else:
        autoLicht.Groen()
        fietsLicht.Rood()
       