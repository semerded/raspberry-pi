"""
volkomen rood stoplicht
gemaakt door Sem Van Broekhoven

"""


from gpiozero import LED, LightSensor # import de componenten uit de library die je nodig hebt
from time import sleep # om delay's toe te voegen
# witregel om de code makkelijker leesbaar te maken
AUTOROOD = LED(10) # duid de led aan op pin 10
AUTOGEEL = LED(9) # duid de led aan op pin 9
AUTOGROEN = LED(11) # duid de led aan op pin 11
# witregel om de code makkelijker leesbaar te maken
FIETSROOD = LED(13) # duid de led aan op pin 13
FIETSGEEL = LED(19) # duid de led aan op pin 19
FIETSGROEN = LED(26) # duid de led aan op pin 26
# witregel om de code makkelijker leesbaar te maken
LDR = LightSensor(21) # zet de LDR op pin 21
# witregel om de code makkelijker leesbaar te maken
class stoplicht: # maak een class aan met de verschillende standen van het stoplicht
    def __init__(self, lichtRood, lichtGeel, lichtGroen) -> None: # maak de class aan en voeg de verschillende lichten toe
        self.__lichtRood = lichtRood # 
        self.__lichtGeel = lichtGeel
        self.__lichtGroen = lichtGroen
# witregel om de code makkelijker leesbaar te maken
# witregel om de code makkelijker leesbaar te maken    
    def Rood(self): # lichtstand rood
        self.__lichtRood.on() # zet lamp aan
        self.__lichtGeel.off()
        self.__lichtGroen.off()
# witregel om de code makkelijker leesbaar te maken    
# witregel om de code makkelijker leesbaar te maken   
    def Geel(self): # lichtstand geel
        self.__lichtRood.off() # zet lamp uit
        self.__lichtGeel.on() # zet lamp aan
        self.__lichtGroen.off() # zet lamp uit
# witregel om de code makkelijker leesbaar te maken
# witregel om de code makkelijker leesbaar te maken       
    def Groen(self): # lichtstand groen
        self.__lichtRood.off() # zet lamp uit
        self.__lichtGeel.off() # zet lamp uit
        self.__lichtGroen.on() # zet lamp aan     
# witregel om de code makkelijker leesbaar te maken
fietsLicht = stoplicht(FIETSROOD, FIETSGEEL, FIETSGROEN) # voeg de standen van de class aan de fietslichten toe
autoLicht = stoplicht(AUTOROOD, AUTOGEEL, AUTOGROEN) # voeg de standen van de class aan de autolichten toe
# witregel om de code makkelijker leesbaar te maken
tijdGeel = 1 # de tijd dat het geel is
tijdGroen = 5 # de tijd dat het groen/rood is
# witregel om de code makkelijker leesbaar te maken
# bij het starten van het programma staan de lichten op rood 
fietsLicht.Rood() # zet fietslicht op rood
autoLicht.Rood() # zet autolicht op rood
sleep(tijdGroen) # tijd dat het licht rood blijft
# witregel om de code makkelijker leesbaar te maken
while True: # de loop die zich zal blijven herhalen
    if LDR.is_active: # als de LDR licht detecteerd
        fietsLicht.Geel() # geel licht voor fietsers
        autoLicht.Geel() # geel licht voor auto's
        sleep(tijdGeel) # tijd dat het geel blijft
        fietsLicht.Groen() # groen licht voor fietsers
        autoLicht.Rood() # rood licht voor auto's
        sleep(tijdGroen) # tijd dat het groen/rood blijft
        fietsLicht.Geel() # geel licht voor fietsers
        autoLicht.Geel() # geel licht voor auto's
        sleep(tijdGeel) # tijd dat het geel blijft
        fietsLicht.Rood() # rood licht voor fietsers
        autoLicht.Groen() # groen licht voor auto's
        sleep(tijdGroen) # tijd dat het groen/rood blijft
    else: # als het donker is
        autoLicht.Groen() # autolicht blijft op groen staan
        fietsLicht.Rood() # fietslicht blijft op rood staan